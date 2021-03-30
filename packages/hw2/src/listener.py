#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

class Listener:
    def __init__(self):
        rospy.Subscriber("total", Float32, self.callback)

    def callback(self,data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    Listener()

    rospy.spin()
