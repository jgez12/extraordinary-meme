#!/usr/bin/env python3
import csv
import rospy
import matplotlib
import math
from duckietown_msgs.msg import WheelsCmdStamped
from duckietown_msgs.msg import Twist2DStamped
from lab4.msg import DistWheel
from lab4.msg import Pose2D

class odom:
	def  __init__(self):
		rospy.Subscriber("wheels_driver_node/wheels_cmd", WheelsCmdStamped, self.integrate)
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
		self.posistion = DistWheel()

	
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
		msg.x = self.x * 0.158
		msg.y = self.y *0.158
		msg.theta = self.theta
		rospy.logwarn(msg)

	def integrate(self,velocity):
		
		self.posistion.dist_wheel_left += velocity.vel_left*0.01
		self.posistion.dist_wheel_right += velocity.vel_right*0.01
		self.deltas(self.posistion)
		
		
		

if __name__ == "__main__":
	try:
		rospy.init_node('odom')
		od = odom()
		rate = rospy.Rate(10000)
		while not rospy.is_shutdown():
			rospy.sleep(2)
			od.talk()
	except rospy.ROSInterruptException:
		pass
			

