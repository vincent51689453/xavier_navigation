# xavier_navigation
It is a navigation package for AGV using NVIDIA Jetson Xavier NX

## Object detection
1. Image Detection

For the first execution, there may be have an error about "No module named 'model'". Therefore, please execute:
```
rosrun torch_object_detection model.py
```

In order to execute single image inferencing, please execute:
```
rosrun torch_object_detection detect_image.py
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