#!/usr/bin/env python3
import rospy
from numpy import arange,sign
from random import random
from std_msgs.msg import Float32
from PID import PID


if __name__ == '__main__':
    try:
        rospy.set_param('controller_ready', 'true')
        rospy.init_node('PID_controller')
        control = PID(kp=0.22, ki=0.05, kd=5.5)
        rospy.Subscriber("error", Float32, control.update_error)
        pub_control = rospy.Publisher("control_input", Float32, queue_size=10)
        rate = rospy.Rate(1000)
        while not rospy.is_shutdown():
            
            
            rospy.set_param('controller_ready', 'true')
            control.controller(0.001)
            pub_control.publish(control.c)
            rate.sleep()
            rospy.logwarn(control.I)
            
    except rospy.ROSInterruptException:
        pass
