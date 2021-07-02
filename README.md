# xavier_navigation
It is a navigation package for AGV using NVIDIA Jetson Xavier NX

## Realsense Installation
1. Install realsense SDK 2.0
```
sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo bionic main" -u
sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev
```
2. Build pyrealsense2 from source for PYTHON2.7
```
cd installLibrealsense
./buildLibrealsense.sh
```
** Remember to add the last line into ~/.bashrc **

After installation, you should be able to see /usr/local/lib/pythoon2.7/pyrealsense2 and /usr/local/lib contains librealsense2 files.

3. Verify installation by realsense-viewer
```
realsense-viewer
```

4. Install ROS realsense package
```
sudo apt-get install ros-$ROS_DISTRO-realsense2-camera
```

In order to start the realsense in ROS, please run
```
./start_realsense.sh
```

## Object detection
1. Image Object Detection

For the first execution, there may be have an error about "No module named 'model'". Therefore, please execute:
```
rosrun torch_object_detection model.py
```

In order to execute single image inferencing, please execute:
```
rosrun torch_object_detection detect_image.py
```

2. Realtime Object Detection
```
rosrun torch_object_detection detect_usb_camera.py
```

![image](https://github.com/vincent51689453/xavier_navigation/blob/melodic-jp4.4/git_image/image_detection.png)

## Image Segmentation
1. Image Segmentation

For performing image segmentation using Mask-RCNN on an image, please execute:
```
rosrun torch_mask_rcnn detect_image.py
```

2. Realtime segmentation with USB camera

For performing realtime segmentation using Mask-RCNN with USB camera, please execute:
```
rosrun torch_mask_rcnn detect_usb_camera.py
```

![image](https://github.com/vincent51689453/xavier_navigation/blob/melodic-jp4.4/git_image/image_segmentation.png)
