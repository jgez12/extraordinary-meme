#!/usr/bin/env python3
import csv
import rospy
from odometry_hw.msg import DistWheel
from odometry_hw.msg import Pose2D
import matplotlib
import math

class odom:
	def  __init__(self):
		self.pub = rospy.Publisher("pose", Pose2D, queue_size=10)
		self.delta_s = None
		self.delta_x = None
		self.delta_y = None
		self.delta_theta = None
		self.x = 0
		self.y = 0
		self.theta = 0
		self.new_x = None
		self.new_y = None
		self.new_theta = None
		rospy.Subscriber("dist_wheel", DistWheel, self.deltas)
	
	def deltas(self,s):
				
		self.delta_s = (s.dist_wheel_left + s.dist_wheel_right)/2
		self.delta_theta = (s.dist_wheel_right - s.dist_wheel_left)/0.1
		self.delta_x = self.delta_s*math.cos(self.theta + self.delta_theta/2)
		self.delta_y = self.delta_s*math.sin(self.theta + self.delta_theta/2)

		

		self.new_x = self.x + self.delta_x
		self.new_y = self.y + self.delta_y
		self.new_theta = self.theta + self.delta_theta
		self.x = self.new_x
		self.y = self.new_y
		self.theta = self.new_theta
		
	def talk(self):
		msg = Pose2D()        
		msg.x = self.x
		msg.y = self.y
		self.pub.publish(msg)
		

if __name__ == "__main__":
	try:
		rospy.init_node('odom_hw7', anonymous=True)
		od = odom()
		
		rate = rospy.Rate(10000)
		while not rospy.is_shutdown():
			rate.sleep()
			od.talk()
	except rospy.ROSInterruptException:
		pass
			

