#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rospy
from cv_bridge import CvBridge
from duckietown_msgs.msg import SegmentList
from duckietown_msgs.msg import Segment
from sensor_msgs.msg import CompressedImage



class LaneDetector:
	def __init__(self):
		self.bridge = CvBridge()
		rospy.Subscriber("camera_node/image/compressed", CompressedImage, self.lines_cb, queue_size=1, buff_size=2 ** 24)
		self.pub = rospy.Publisher("/charlieconway/line_detector_node/segment_list", SegmentList, queue_size=10)



	def lines_cb(self, image):
		img = self.bridge.compressed_imgmsg_to_cv2(image, "bgr8")
		imgCropped = img[240:480, 0:640]
		hsvimg = cv.cvtColor(imgCropped, cv.COLOR_BGR2HSV)
		lower = np.array([23, 157, 118])
		upper = np.array([179, 255, 255])
		white_lower = np.array([42, 8, 88])
		white_upper = np.array([122, 99, 255])
		arr_cutoff = np.array([0, 40, 0, 40])
		arr_ratio = np.array([1/160, 1/120, 1/160, 1/120])
		a = []
		b = []
		c = SegmentList()
		
		maskWhite = cv.inRange(hsvimg, white_lower, white_upper)
		maskYellow = cv.inRange(hsvimg, lower, upper)
			
		imgWhite = cv.bitwise_and(imgCropped, imgCropped, mask=maskWhite)
		imgYellow = cv.bitwise_and(imgCropped, imgCropped, mask=maskYellow)
		imgCanny_white = cv.Canny(imgWhite, 150, 200)
		imgCanny_yellow = cv.Canny(imgYellow, 150, 200)        
		imgResized_white = cv.resize(imgCanny_white, (160, 120), interpolation=cv.INTER_NEAREST)
		imgResized_yellow = cv.resize(imgCanny_yellow, (160, 120), interpolation=cv.INTER_NEAREST)
		imgCut_white = imgResized_white[40:120, 0:160]
		imgCut_yellow = imgResized_yellow[40:120, 0:160]
		lines_white = cv.HoughLinesP(imgCut_white, 1, (3.14159 / 180), 1)
		lines_yellow = cv.HoughLinesP(imgCut_yellow, 1, (3.14159 / 180), 1)
		#rospy.logwarn(maskYellow)
		
		for i in range(len(lines_white)):
			lines_normalized_white = (lines_white[i] + arr_cutoff) * arr_ratio
			a.append(lines_normalized_white)
		for i in range(len(lines_yellow)):
			lines_normalized_yellow = (lines_yellow[i] + arr_cutoff) * arr_ratio
			b.append(lines_normalized_yellow)

		
		segments = SegmentList()
		white_seg = Segment()
		yellow_seg = Segment()
		for i in range(len(a)):
			lines_a = a[i][0]	
			white_seg.color = 0
			white_seg.pixels_normalized[0].x = lines_a[0]
			white_seg.pixels_normalized[0].y = lines_a[1]
			white_seg.pixels_normalized[1].x = lines_a[2]
			white_seg.pixels_normalized[1].y = lines_a[3]
			segments.segments.append(white_seg)


		for i in range(len(b)):
			lines_b = b[i][0]
			yellow_seg.color = 1
			yellow_seg.pixels_normalized[0].x = lines_b[0]
			yellow_seg.pixels_normalized[0].y = lines_b[1]
			yellow_seg.pixels_normalized[1].x = lines_b[2]
			yellow_seg.pixels_normalized[1].y = lines_b[3]
			#yellow_seg.append([yellow_seg.pixels_normalized[0].x,yellow_seg.pixels_normalized[0].y,yellow_seg.pixels_normalized[1].x,yellow_seg.pixels_normalized[1].y])
			segments.segments.append(yellow_seg)

		#rospy.logwarn(lines_yellow)
		self.pub.publish(segments)




if __name__ == "__main__":
	try:	
		rospy.init_node("lane_detector")
		r = rospy.Rate(20)
		while not rospy.is_shutdown():
			rospy.sleep(2)
			LD = LaneDetector()
			rospy.logwarn("Jacob Gesualdi lane detector")
			
	except rospy.ROSInterruptException:
		pass
