import setup_path
import airsim

import pygame, sys
import numpy as np
import os
import tempfile
import pprint
import cv2
import time

import rospy
import rosbag
from sensor_msgs.msg import Imu as Imu_msg

pygame.init()
# rostopic names in this file：
topics = ["/airsim_node/drone_1/imu/Imu","/airsim_node/drone_1/odom_local_ned"]
# output file name：
# IMU+GT bag name
bag_output_name = "Airsim_Imu_GT_Car_10m_s_turn_2.bag"
# GT TUM FORMAT
gt_output_name = "./ground_truth_Car_10m_s_turn_2.txt"
output_handle = rosbag.Bag(bag_output_name,'w')
output_gt = open(gt_output_name,'w')


# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
print("API Control enabled: %s" % client.isApiControlEnabled())
car_controls = airsim.CarControls()

time_start = time.time()
seq = 0
data = client.getImuData('imu','drone_1')
data_slow = data
ground_truth = client.simGetGroundTruthKinematics('drone_1')
display = pygame.display.set_mode((100, 100))
finish = 0
while(finish == 0):
    time.sleep(1e-5)
    temp = client.getImuData('imu','drone_1')
    if(abs(temp.time_stamp - data.time_stamp)/1e9 > 0.001):
        # print(abs(temp.time_stamp - data.time_stamp)/1e9)
        msg = Imu_msg()
        msg.header.stamp.secs = int(temp.time_stamp / 1000000000)
        msg.header.stamp.nsecs = temp.time_stamp % int(1e9)
        msg.header.frame_id = 'drone_1'

        msg.angular_velocity.x = temp.angular_velocity.x_val
        msg.angular_velocity.y = temp.angular_velocity.y_val
        msg.angular_velocity.z = temp.angular_velocity.z_val

        msg.linear_acceleration.x = temp.linear_acceleration.x_val
        msg.linear_acceleration.y = temp.linear_acceleration.y_val
        msg.linear_acceleration.z = temp.linear_acceleration.z_val

        msg.orientation.x  = temp.orientation.x_val
        msg.orientation.y  = temp.orientation.y_val
        msg.orientation.z  = temp.orientation.z_val
        msg.orientation.w  = temp.orientation.w_val

        if(abs(temp.time_stamp - data_slow.time_stamp)/1e9 > 0.004):
            print(abs(temp.time_stamp - data_slow.time_stamp)/1e9)
            msg.header.seq = seq
            seq = seq + 1
            output_handle.write(topics[0],msg,t=msg.header.stamp)
            data_slow = temp
            ground_truth = client.simGetGroundTruthKinematics('drone_1')
            str = "%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n" % (temp.time_stamp / 1000000000, ground_truth.position.x_val, ground_truth.position.y_val, ground_truth.position.z_val, ground_truth.orientation.x_val, ground_truth.orientation.y_val, ground_truth.orientation.z_val, ground_truth.orientation.w_val)
            output_gt.write(str)
        # msg.header.seq = seq
        # seq = seq + 1
        # output_handle.write(topics[0],msg,t=msg.header.stamp)
        # ground_truth = client.simGetGroundTruthKinematics('drone_1')
        
        # str = "%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n" % (temp.time_stamp / 1000000000, ground_truth.position.x_val, ground_truth.position.y_val, ground_truth.position.z_val, ground_truth.orientation.x_val, ground_truth.orientation.y_val, ground_truth.orientation.z_val, ground_truth.orientation.w_val)
        # output_gt.write(str)

        data = temp
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN): 
            print("Record Finished!")
            finish = 1


output_handle.close()
airsim.wait_key('Press any key to reset to original state')

client.reset()
client.armDisarm(False)

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)