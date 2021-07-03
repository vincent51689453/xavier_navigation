# xavier_navigation
It is a navigation package for AGV using NVIDIA Jetson Xavier NX

## Environmental Setup
### Realsense Installation
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

### Pytorch Installation for python2
Please execute the following to install pytorch v1.4.0 for python2 and ROS melodic
```
wget https://nvidia.box.com/shared/static/1v2cc4ro6zvsbu0p8h6qcuaqco1qcsif.whl -O torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
sudo apt-get install libopenblas-base libopenmpi-dev 
pip install future torch-1.4.0-cp27-cp27mu-linux_aarch64.whl
```

Afterward, torchvision v0.5.0 can be intalled by the following as well.
```
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
git clone --branch v0.5.0 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
cd torchvision
export BUILD_VERSION=0.5.0  # where 0.5.0 is the torchvision version  
sudo python setup.py install
cd ../  # attempting to load torchvision from build dir will result in import error
pip install 'pillow<7' # always needed for Python 2.7, not needed torchvision v0.5.0+ with Python 3.6
```

### VSCode Installation
After downloading the debian package from https://code.visualstudio.com/Download
```
sudo dpkg -i <vscode_package>.dep
sudo apt install apt-transport-https
sudo apt update
sudo apt install code
#start vscode
code 
```

## System Packages
### Object detection
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

### Image Segmentation
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

3. Realtime segmentation with Realsense D435i
```
./start_realsense_publish.sh
./start_realsnese_maskrcnn.sh
```

![image](https://github.com/vincent51689453/xavier_navigation/blob/melodic-jp4.4/git_image/image_segmentation.png)

## Visualization
1. RQT Multiple Image viewer
```
./rqt_tools.sh
```
