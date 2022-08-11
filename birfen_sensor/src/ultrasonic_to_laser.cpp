#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <sensor_msgs/Range.h>

using namespace std;

float dist = std::numeric_limits<float>::infinity();



void RangeMessageReveived(const sensor_msgs::Range::ConstPtr& range){
    if (range->range > range->min_range && range->range < range->max_range){
        dist = range->range;
    }
}

void ScanMessageReveived(const sensor_msgs::LaserScan::ConstPtr& scan){

    ros::NodeHandle n3;

    ros::Publisher scan_pub = n3.advertise<sensor_msgs::LaserScan>("scan2", 500);
    ros::Rate loop_rate(10);

    sensor_msgs::LaserScan m_scan;
    m_scan.header.stamp = scan->header.stamp;
    m_scan.header.frame_id = scan->header.frame_id;
    m_scan.angle_min = scan->angle_min;
    m_scan.angle_max = scan->angle_max;
    m_scan.angle_increment = scan->angle_increment;
    m_scan.time_increment = scan->time_increment;
    m_scan.range_min = scan->range_min;
    m_scan.range_max = scan->range_max;
    m_scan.intensities = scan->intensities;

    m_scan.ranges.resize(720);

    m_scan.ranges = scan->ranges;

    for(int i = 50; i<116; i++){
        if(m_scan.ranges[i] > dist || m_scan.ranges[i] == std::numeric_limits<float>::infinity()){
            m_scan.ranges[i] = dist;
        }
    }

    scan_pub.publish(m_scan);
    ROS_INFO("published");
    loop_rate.sleep();
    ros::spinOnce();
}


int main(int argc, char** argv){
    ros::init(argc, argv, "sensor_merger");

    ros::NodeHandle n1;
    ros::Subscriber sub = n1.subscribe("/scan", 1000, ScanMessageReveived);

    ros::NodeHandle n2;
    ros::Subscriber sub2 = n2.subscribe("/sensor/ir_front", 1000, RangeMessageReveived);

    ros::spin();


}