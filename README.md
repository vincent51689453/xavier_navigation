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