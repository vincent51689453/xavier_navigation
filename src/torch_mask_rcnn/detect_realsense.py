#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author : Chan Tai Wing
@Date   : 01 Jun 2021
@About  : Publish/Subscribe of realsense images
"""
#System Packages
import sys
import os
import cv2
import numpy as np
import pyrealsense2 as rs2
import time
from pynput import keyboard
import torch
import torchvision
from PIL import Image
from torchvision import transforms as T
import matplotlib.pyplot as plt
import random

#ROS Packages
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge, CvBridgeError

#Customize packages
import node_config as NC
import maskrcnn_rs2 as maskrcnn

tick_sign = u'\u2714'.encode('utf8')
cross_sign = u'\u274c'.encode('utf8')

# Indicate CUDA processor
def cuda_setup():
    device = torch.cuda.current_device()
    torch.cuda.set_device(device)


# System Relase based on keyboard input
def on_press (key):
    try:
        if((key.char=='q')or(key.char=='Q')):
            NC.system_release = True
   
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        p = 0

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def depth_callback(ros_msg):
    # Depth image callback
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(ros_msg)
    depth_array = np.array(image, dtype=np.float32)
    NC.depth_image = image
    NC.depth_array = depth_array
    #Display
    #cv2.imshow('depth_image',image)
    #cv2.waitKey(1)

def color_callback(ros_msg):
    # RGB image callback
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(ros_msg)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    image = cv2.resize(image,(640,480))
    NC.color_image = image
    # Display
    #cv2.imshow('rgb_image',NC.color_image)
    #cv2.waitKey(1)    

def camera_info_callback(cameraInfo):
    NC.intrinsic = rs2.intrinsics()
    # Number of rows and columns in an image
    NC.intrinsic.width = cameraInfo.width
    NC.intrinsic.height = cameraInfo.height

    # Pixels coordinates of the principal point (center of projection)
    NC.intrinsic.ppx = cameraInfo.K[2]
    NC.intrinsic.ppy = cameraInfo.K[5]

    # Focal Length of image (multiple of pixel width and height)
    NC.intrinsic.fx = cameraInfo.K[0]
    NC.intrinsic.fy = cameraInfo.K[4]

    NC.model = rs2.distortion.none
    NC.coeffs = [i for i in cameraInfo.D]


def main():
    global training

    # Image Publisher for color and depth images
    image_pub_color = rospy.Publisher(NC.maskrcnn_rgb_image_topic,Image,queue_size=10)
    image_pub_depth = rospy.Publisher(NC.maskrcnn_depth_image_topic ,Image,queue_size=10)
    bridge = CvBridge()

    # Subscribe color and depth image
    rospy.Subscriber(NC.depth_image_topic,Image,callback=depth_callback)
    rospy.Subscriber(NC.color_image_topic,Image,callback=color_callback)

    # Subscribe camera info [depth_rgb aligned]
    rospy.Subscriber(NC.camera_info_depth_aligned_color_topic,CameraInfo,callback=camera_info_callback)

    # Keyboard Listener
    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    listener.start()
    print("[INFO] You can press <Q> or <q> to end the AI")

	# Load MaskRCNN model and choose inference mode
    cuda_setup()
    print("CUDA setup ... " + tick_sign)
    NC.detect_mode = 1
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    model.cuda()
    print("MaskRCNN initialization... " + tick_sign)
    
    # 2D/3D Image processing
    while not(NC.system_release):
        if((NC.depth_image is not None)and(NC.color_image is not None)):
            
            # Unsupervised Segmentation (RGB):
            color_output = maskrcnn.core(model, NC.color_image, threshold=0.5, rect_th=1, text_th=1, text_size=1)
            #color_output = NC.color_image
            # Visulaiztion in RVIZ
            image_pub_color.publish(bridge.cv2_to_imgmsg(color_output, "bgr8"))
            #image_pub_depth.publish(bridge.cv2_to_imgmsg(depth_output, "bgr8"))
            # Visualization in new window
            # cv2.imshow("Realsense [RGB]",color_output)
            # cv2.imshow("Realsense [Depth]",depth_output)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
   
    # Release GPU memory
    torch.cuda.empty_cache()
    print("GPU Memroy is released " + tick_sign)


if __name__ == '__main__':
    rospy.init_node(NC.node_name)
    main()
