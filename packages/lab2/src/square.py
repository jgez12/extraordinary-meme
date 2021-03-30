#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped

class Square:
    def __init__(self):
        self.pub = rospy.Publisher('/gordonbombay/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=10)
    def straight(self):
        msg = Twist2DStamped()        
        msg.v = 0.35
        msg.omega = 0
        self.pub.publish(msg)
    def turn(self):
        msg = Twist2DStamped()        
        msg.v = 0
        msg.omega = 2.1
        self.pub.publish(msg)
        
        
        
        

if __name__ == '__main__':
    try:
        s = Square()
        rospy.init_node ('square')
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            s.straight()
            rate.sleep()
            rate.sleep()
            s.turn()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
