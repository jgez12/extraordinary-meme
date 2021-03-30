#!/usr/bin/env python3
import rospy
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import LanePose
from PID import PID




class angular:
    def __init__(self):
        self.pub = rospy.Publisher('/charlieconway/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=10)
    def talk(self,omega):
        self.msg = Twist2DStamped()
        self.msg.omega = omega
        self.msg.v = 0.1
        self.pub.publish(self.msg)
        rospy.loginfo("publishing message")

class callback:
    def __init__(self):
        rospy.Subscriber('/charlieconway/lane_filter_node/lane_pose', LanePose, self.listen)
        self.phi = 0
        self.d = 0
    def listen(self, mesg):
        self.mesg = LanePose()
        self.d = mesg.d
        self.phi = mesg.phi
        rospy.loginfo('d =%s',self.d)
        rospy.loginfo('phi =%s',self.phi)
    def phi_error(self):        
        control_phi.update_error(self.phi)
        control_phi.controller(0.0001)
        rospy.loginfo('phi after PID =%s',control_phi.c)
        return control_phi.c
    def d_error(self):        
        control_d.update_error(self.d)
        control_d.controller(0.0001)
        rospy.loginfo('d after pid =%s',control_d.c)
        return control_d.c
    def pid_total(self):
        pid_total = self.d_error() + self.phi_error()
        rospy.loginfo('PID total = %s',pid_total)
        return pid_total
if __name__ == '__main__':
    try:
        c = callback()
        rospy.init_node('PID_controller_car')
        rate = rospy.Rate(10000)
        control_d = PID (kp=1.8, ki=0, kd=0)
        control_phi = PID(kp=1.8, ki=0, kd=0)
        while not rospy.is_shutdown():

            
            rospy.sleep(2)
            b = c.pid_total()
            rospy.logwarn("Jacob Gesualdi lane following code")
            rospy.logwarn(c.phi)
            a = angular()
            a.talk(omega=b)
            
            

    except rospy.ROSInterruptException:
        pass

            
    
