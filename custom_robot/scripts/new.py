#! /usr/bin/env python3

from cmath import inf
import rospy
from sensor_msgs.msg import LaserScan, Range

#338 384 ultrasonic sensor  

range_sensor = inf

def laser_callback(msg):

    j = 0
    for i in msg.ranges:

        j+=1
        if i != inf:
            print(j)
    print(j)


if __name__ == '__main__':

    rospy.init_node('us_to_scan')
    sub = rospy.Subscriber('/scan', LaserScan, laser_callback)
    rospy.spin()