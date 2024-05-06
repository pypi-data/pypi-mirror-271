import pathlib

import cv2
import numpy as np
import csv
import threading

from .. import config
from .. import utils
from ._image_gui import GUI, generic_tooltip, qns_tooltip


stopAllProcessing = False
def process(working_dir, config_dir=None, show_visualization=False, show_rejected_markers=False):
    # if show_visualization, each frame is shown in a viewer, overlaid with info about detected markers and poster
    # if show_rejected_markers, rejected ArUco marker candidates are also shown in the viewer. Possibly useful for debug
    working_dir  = pathlib.Path(working_dir)
    if config_dir is not None:
        config_dir = pathlib.Path(config_dir)

    print('processing: {}'.format(working_dir.name))

    # if we need gui, we run processing in a separate thread (GUI needs to be on the main thread for OSX, see https://github.com/pthom/hello_imgui/issues/33)
    if show_visualization:
        gui = GUI(use_thread = False)
        gui.set_interesting_keys('qns')
        gui.register_draw_callback('status',lambda: generic_tooltip(qns_tooltip()))
        gui.add_window(working_dir.name)

        proc_thread = threading.Thread(target=do_the_work, args=(working_dir, config_dir, gui, show_rejected_markers))
        proc_thread.start()
        gui.start()
        proc_thread.join()
        return stopAllProcessing
    else:
        return do_the_work(working_dir, config_dir, None, False)


def do_the_work(working_dir, config_dir, gui, show_rejected_markers):
    global stopAllProcessing
    show_visualization = gui is not None

    utils.update_recording_status(working_dir, utils.Task.Markers_Detected, utils.Status.Running)

    # open file with information about Aruco marker and Gaze target locations
    validationSetup = config.get_validation_setup(config_dir)

    # open video file, query it for size
    inVideo = working_dir / 'worldCamera.mp4'
    if not inVideo.is_file():
        inVideo = working_dir / 'worldCamera.avi'
    cap     = utils.CV2VideoReader(inVideo, utils.get_timestamps_from_file(working_dir / 'frameTimestamps.tsv'))
    width   = cap.get_prop(cv2.CAP_PROP_FRAME_WIDTH)
    height  = cap.get_prop(cv2.CAP_PROP_FRAME_HEIGHT)

    # get info about markers on our poster
    poster          = utils.Poster(config_dir, validationSetup)
    centerTarget    = poster.targets[validationSetup['centerTarget']].center
    # turn into aruco board object to be used for pose estimation
    arucoBoard      = poster.getArucoBoard()

    # setup aruco marker detection
    parameters      = cv2.aruco.DetectorParameters()
    parameters.markerBorderBits       = validationSetup['markerBorderBits']
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    aruco_detector  = cv2.aruco.ArucoDetector(poster.aruco_dict, parameters)

    # get camera calibration info
    cameraMatrix,distCoeff = utils.readCameraCalibrationFile(working_dir / "calibration.xml")[0:2]
    hasCameraMatrix = cameraMatrix is not None
    hasDistCoeff    = distCoeff is not None

    # get interval coded to be analyzed, if any
    analyzeFrames   = utils.readMarkerIntervalsFile(working_dir / "markerInterval.tsv")
    hasAnalyzeFrames= analyzeFrames is not None

    # prep output file
    csv_file = open(working_dir / 'posterPose.tsv', 'w', newline='')
    csv_writer = csv.writer(csv_file, delimiter='\t')
    header = utils.PosterPose.getWriteHeader()
    csv_writer.writerow(header)

    stopAllProcessing = False
    armLength = poster.markerSize/2 # arms of axis are half a marker long
    subPixelFac = 8   # for sub-pixel positioning
    last_frame_idx = -1
    while True:
        # process frame-by-frame
        done, frame, frame_idx, frame_ts = cap.read_frame()
        if frame_idx is not None and frame_idx-last_frame_idx>1:
            print(f'Frame discontinuity detected (jumped from {last_frame_idx} to {frame_idx}), there are probably corrupt frames in your video')
        last_frame_idx = frame_idx

        # check if we're done
        if done or (hasAnalyzeFrames and frame_idx > analyzeFrames[-1]):
            # done
            break
        if frame_idx%100==0:
            print('  frame {}'.format(frame_idx))
        if frame is None:
            # we don't have a valid frame, continue to next
            continue

        if show_visualization:
            keys = gui.get_key_presses()
            if 'q' in keys:
                # quit fully
                stopAllProcessing = True
                break
            if 'n' in keys:
                # goto next
                break

        if hasAnalyzeFrames:
            # check we're in a current interval, else skip processing
            # NB: have to spool through like this, setting specific frame to read
            # with cap.set(cv2.CAP_PROP_POS_FRAMES) doesn't seem to work reliably
            # for VFR video files
            inIval = False
            for f in range(0,len(analyzeFrames),2):
                if frame_idx>=analyzeFrames[f] and frame_idx<=analyzeFrames[f+1]:
                    inIval = True
                    break
            if not inIval:
                # no need to process this frame
                continue

        # detect markers, undistort
        corners, ids, rejectedImgPoints = aruco_detector.detectMarkers(frame)
        recoveredIds = None

        if np.all(ids != None):
            if len(ids) >= validationSetup['minNumMarkers']:
                pose = utils.PosterPose(frame_idx)

                # get camera pose
                if hasCameraMatrix and hasDistCoeff:
                    # Refine detected markers (eliminates markers not part of our poster, adds missing markers to the poster)
                    corners, ids, rejectedImgPoints, recoveredIds = utils.arucoRefineDetectedMarkers(aruco_detector,
                            image = frame, arucoBoard = arucoBoard,
                            detectedCorners = corners, detectedIds = ids, rejectedCorners = rejectedImgPoints,
                            cameraMatrix = cameraMatrix, distCoeffs = distCoeff)

                    objP, imgP = arucoBoard.matchImagePoints(corners, ids)
                    pose.nMarkers = 0 if objP is None else int(objP.shape[0]/4)
                    if pose.nMarkers>0:
                        pose.poseOk, pose.rVec, pose.tVec = cv2.solvePnP(objP, imgP, cameraMatrix, distCoeff, np.empty(1), np.empty(1))

                    # draw pose if wanted
                    if pose.poseOk and show_visualization:
                        # draw axis indicating poster pose (origin and orientation)
                        utils.drawOpenCVFrameAxis(frame, cameraMatrix, distCoeff, pose.rVec, pose.tVec, armLength, 3, subPixelFac)

                # also get homography (direct image plane to plane in world transform). Use undistorted marker corners
                if hasCameraMatrix and hasDistCoeff:
                    cornersU = [cv2.undistortPoints(x, cameraMatrix, distCoeff, P=cameraMatrix) for x in corners]
                else:
                    cornersU = corners
                H, status = utils.estimateHomography(poster.knownMarkers, cornersU, ids)

                if status:
                    pose.hMat = H
                    pose.nMarkersH = len(cornersU)
                    if show_visualization:
                        # find where target is expected to be in the image
                        iH = np.linalg.inv(pose.hMat)
                        target = utils.applyHomography(iH, centerTarget[0], centerTarget[1])
                        if hasCameraMatrix and hasDistCoeff:
                            target = utils.distortPoint(*target, cameraMatrix, distCoeff)
                        # draw target location on image
                        if target[0] >= 0 and target[0] < width and target[1] >= 0 and target[1] < height:
                            utils.drawOpenCVCircle(frame, target, 3, (0,0,0), -1, subPixelFac)

                if pose.poseOk or status:
                    csv_writer.writerow( pose.getWriteData() )

            # if any markers were detected, draw where on the frame
            if show_visualization:
                utils.drawArucoDetectedMarkers(frame, corners, ids, subPixelFac=subPixelFac, specialHighlight=[recoveredIds,(255,255,0)])

        # for debug, can draw rejected markers on frame
        if show_visualization and show_rejected_markers:
            cv2.aruco.drawDetectedMarkers(frame, rejectedImgPoints, None, borderColor=(211,0,148))

        if show_visualization:
            # keys is populated above
            if 's' in keys:
                # screenshot
                cv2.imwrite(str(working_dir / ('detect_frame_%d.png' % frame_idx)), frame)
            gui.update_image(frame, frame_ts/1000., frame_idx)
            closed, = gui.get_state()
            if closed:
                stopAllProcessing = True
                break

    csv_file.close()
    if show_visualization:
        gui.stop()

    utils.update_recording_status(working_dir, utils.Task.Markers_Detected, utils.Status.Finished)

    return stopAllProcessing