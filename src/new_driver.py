#!/usr/bin/env python3

# simple controller that subscribes to base_scan and publishes to cmd_vel

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# The topic we'll use to control the robot
command_topic = '/cmd_vel'

# topic with laser data
laser_topic = '/base_scan'

# initialize node and publisher
rospy.init_node('new_driver', anonymous=True)
controller = rospy.Publisher(command_topic, Twist, queue_size=10)

def callback(msg):

    straight_ahead = msg.ranges[135]
    acute_L = msg.ranges[180]
    acute_R = msg.ranges[90]

    cmd_vel = Twist()

    if(straight_ahead < 1 or acute_L < 1 or acute_R < 1):
        cmd_vel.linear.x = 0
        cmd_vel.angular.z = 1.0
    else:
        cmd_vel.linear.x = 1.0
        cmd_vel.angular.z = 0.0

    controller.publish(cmd_vel)


def main():

    # nitialize subscriber
    sub = rospy.Subscriber(laser_topic,LaserScan,callback)
    hz = 10  # refresh rate in Hz
    rate = rospy.Rate(hz)
    rospy.spin()

try:
    main()
except rospy.ROSInterruptException:
    pass
