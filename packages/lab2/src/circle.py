#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped

class Circle:
    def __init__(self):
        self.pub = rospy.Publisher('/gordonbombay/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=10)
    def talk(self):
        msg = Twist2DStamped()        
        msg.v = 0.5
        msg.omega = 0.5
        self.pub.publish(msg)
        
        
        
        

if __name__ == '__main__':
    try:
        c = Circle()
        rospy.init_node ('circle')
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            c.talk()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
