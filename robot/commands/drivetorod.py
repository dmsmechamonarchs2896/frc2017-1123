import wpilib
from wpilib.command import Command

import subsystems

import logging

logging.basicConfig(level=logging.DEBUG)


class DriveToRod(Command):
    '''
    This command will find the rod and drive the robot towards it.
    '''

    def __init__(self):
        super().__init__("Drive To Rod")

        self.requires(subsystems.front_camera)

    def execute(self):
        pass

    def get_center(self):
        time, frame = subsystems.front_camera.cv_sink.grabFrame(subsystems.front_camera.processing_frame)
        if time == 0:
            print("error:", subsystems.front_camera.cv_sink.getError())
            return

        # filter only green
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([45, 140, 100]), np.array([65, 210, 130]))

        # find relevant retroreflective tape contours
        contours = cv2.findContours(mask, cv2.cv.CV_RETR_TREE, cv2.cv.CV_CHAIN_APPROX_SIMLE)[0]
        # find two largest four-sided contours
        largest = (0, 0)  # (contour, area)
        second_largest = (0, 0)  # (contour, area)
        for c in contours:
            area = cv2.contourArea(c)
            if area < 100:  # remove noise
                continue
            perim = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, .05 * perim, True)
            if len(approx) != 4:  # only consider quadrilaterals
                continue
            if area > largest[1]:
                second_largest = largest
                largest = (c, area)
            elif area > second_largest[1]:
                second_largest = (c, area)

        if second_largest[0] == 0:  # if did not find the tape strips
            return False

        # find position of rod
        moments1 = cv2.moments(largest[0])
        center1 = (moments1['m10'] // moments1['m00'], moments1['m01'] // moments1['m00'])  # center of first tape strip
        moments2 = cv2.moments(second_largest[0])
        center2 = (
        moments2['m10'] // moments2['m00'], moments2['m01'] // moments2['m00'])  # center of second tape strip

        return ((center1[0] + center2[0]) // 2, (center1[1] + center2[1]) // 2)
