#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

class Talker:
    def __init__(self):
        self.pub = rospy.Publisher('chatter', Float32, queue_size=10)
    def talk(self):
        input_value = 0
        rospy.loginfo(input_value)
        self.pub.publish(input_value)
        	

if __name__ == '__main__':
    try:
        t = Talker()
        rospy.init_node ('talker')
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            t.talk()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
    
