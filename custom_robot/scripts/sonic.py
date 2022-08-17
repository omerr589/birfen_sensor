#! /usr/bin/env python3

from cmath import inf
import rospy
from sensor_msgs.msg import LaserScan, Range
import tf

# 345 to 389 ultrasonic sensor  

range_sensor = inf

def range_callback(msg):
    global range_sensor
    if msg.range < msg.max_range and msg.range > msg.min_range:
        range_sensor = msg.range


# timer_callback
def laser_callback(msg):
    global range_sensor
    scan = LaserScan()

    listener = tf.TransformListener()
    try:
        (trans,rot) = listener.lookupTransform('laser_frame', 'ultrasonic_sensor_link', rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException):
        pass

    print(trans)
    
    
    scan.header.stamp = msg.header.stamp
    scan.header.frame_id = msg.header.frame_id
    scan.angle_min = msg.angle_min
    scan.angle_max = msg.angle_max
    scan.angle_increment = msg.angle_increment
    scan.time_increment = msg.time_increment
    scan.range_min = msg.range_min
    scan.range_max = msg.range_max
    scan.intensities = msg.intensities

    scan.ranges[0:len(msg.ranges)-1] = msg.ranges[0:len(msg.ranges)-1]
    for i in range(0, len(msg.ranges)-1):
        if i < 389 and i > 345 and range_sensor < msg.ranges[i]:
            scan.ranges[i] = range_sensor +trans[0]

        
    pub = rospy.Publisher('/scan2', LaserScan, queue_size=5)
    rate = rospy.Rate(100) # 10hz
    pub.publish(scan)
    rate.sleep()


if __name__ == '__main__':

    rospy.init_node('us_to_scan')
    sub = rospy.Subscriber('/scan', LaserScan, laser_callback)
    sub2 = rospy.Subscriber('/ir_sensor', Range, range_callback)
    rospy.spin()