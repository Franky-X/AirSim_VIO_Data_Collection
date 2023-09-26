#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""

author: Chaoran Xiong


"""
import rospy
import rosbag
import time
from sensor_msgs.msg import Image as Image_msg
import cv2
import cv_bridge
import numpy as np

call_back = 0

# input IMU+GT bag name:
bag_file_name = "/home/frankxcr/AirSim/PythonClient/car/Airsim_Imu_GT_Car_10m_s_turn.bag"
# rostopic names in this file：
topics = ["/airsim_node/drone_1/front_left_custom/Scene","/airsim_node/drone_1/front_right_custom/Scene","/airsim_node/drone_1/imu/Imu","/airsim_node/drone_1/odom_local_ned"]
# output IMU+Cam name：
bag_output_name = "Airsim_whole_pack_Car_10m_s_turn.bag"

bag_handle = rosbag.Bag(bag_file_name,'r')
output_handle = rosbag.Bag(bag_output_name,'w')
time_start=time.time()

def image_topic_process(msg,topic,output_handle):
    '''
    :param msg: image topic
    :param topic: topic name
    :param output_handle: output file handle
    '''
    t = msg.header.stamp
    if (t.secs>0) and (t.nsecs>0) and msg.height > 0 and msg.width > 0:
        output_handle.write(topic,msg,t=msg.header.stamp)
    else:
        print("Catched!")
    return
### go through all the topics：
flag = 0
for topic, msg, t in bag_handle.read_messages(topics):
    print(topic)
    print(msg.header.stamp)
    if (topic==topics[3]):
        #msg.linear_acceleration.z = -9.81
        #output_handle.write(topic,msg,t=msg.header.stamp)
        print('odo')
    else: 
        if(topic==topics[2]):
            output_handle.write(topic,msg, t=msg.header.stamp)
            if(call_back % 10 == 0):
                # Change str to your own png Dir
                str = "/home/frankxcr/airsim_drone_10m_s_turn/0/%d_0.png" % call_back
                print(str)
                img_msg = Image_msg()
                img = cv2.imread(str)
                if(img is not None):
                    # cv2.imshow("Image window Right",img)
                    img_msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, "bgr8")
                    img_msg.header = msg.header
                    temp_time = img_msg.header.stamp.to_sec()
                    # if(call_back / 10 < 10): 
                    temp_time = temp_time + 0.0
                    print(temp_time)
                    # img_msg.header.stamp.nsecs = img_msg.header.stamp.nsecs + int(1e9*(0.005))
                    img_msg.header.stamp = img_msg.header.stamp.from_sec(temp_time)
                    img_msg.height, img_msg.width = 480, 640
                    output_handle.write(topics[1],img_msg,t=img_msg.header.stamp)
                # Change str to your own png Dir
                str = "/home/frankxcr/airsim_drone_10m_s_turn/1/%d_1.png" % call_back
                print(str)
                # img_msg = Image_msg()
                img = cv2.imread(str)
                if(img is not None):
                    # cv2.imshow("Image window Left",img)
                    # cv2.waitKey(3)
                    img_msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, "bgr8")
                    img_msg.header = msg.header
                    # temp_time = img_msg.header.stamp.to_sec()
                    # temp_time = temp_time - 0.005
                    print(temp_time)
                    # img_msg.header.stamp.nsecs = img_msg.header.stamp.nsecs + int(1e9*(0.005))
                    img_msg.header.stamp = img_msg.header.stamp.from_sec(temp_time)
                    print(img_msg.header.stamp)
                    output_handle.write(topics[0],img_msg,t=img_msg.header.stamp)
            call_back = call_back + 1
    
output_handle.close()
time_end=time.time()
print('time cost',time_end-time_start,'s')
