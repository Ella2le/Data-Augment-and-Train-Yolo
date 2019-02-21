#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
import cv2
from matplotlib import pyplot as plt
from open3d import *
import time
import os, sys
PYTHON_FILE_PATH = os.path.join(os.path.dirname(__file__))+"/"

# ROS
import rospy
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String

# my libriries
sys.path.append(PYTHON_FILE_PATH + "../src_python")
from lib_cloud import read_color_depth_images
from lib_ros_topic import CameraInfoPublisher, ImagePublisher

# ==================================================================================================


if __name__=="__main__":
    rospy.init_node("n0_fake_rgbd_image_publisher")
    rospy.sleep(0.5)
    bridge = CvBridge()

    # Get color and depth image
    images_folder = "/home/feiyu/baxterws/src/winter_prj/auto_collect/data/mydata"
    image_index=1
    color_img, depth_img = read_color_depth_images(images_folder, image_index, img_format="cv")

    # Get camera info
    topic_camera_info = rospy.get_param("topic_camera_info")
    camera_intrinsic = read_pinhole_camera_intrinsic(rospy.get_param("file_camera_info"))

    # # Set publisher
    color_pub = ImagePublisher(rospy.get_param("topic_color_image"), "color")
    depth_pub = ImagePublisher(rospy.get_param("topic_depth_image"), "depth")
    cam_info_pub = CameraInfoPublisher(rospy.get_param("topic_camera_info"))
    
    # Publish image
    cnt=0
    while not rospy.is_shutdown():
        cnt+=1

        color_pub.publish(color_img)
        depth_pub.publish(depth_img)
        cam_info_pub.publish_open3d_format(camera_intrinsic)

        # print "node 1: pub data {:04d}...".format(cnt)
        rospy.sleep(3.0)
    print "Node0 stops"

    