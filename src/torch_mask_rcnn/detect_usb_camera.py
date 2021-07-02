#!/usr/bin/env python
import torch
import torchvision
from PIL import Image
from torchvision import transforms as T
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import maskrcnn
# pip3 install torchvision==0.5.0
# sudo apt-get install python3-matplotlib
#Checkpoint path: /home/xavier/.cache/torch/checkpoints/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth

# 0 -> image / 1 -> usb camera
maskrcnn.detect_mode = 1

# Load model checkpoint
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Setup camera
camera = cv2.VideoCapture(0)

# Loop
while True:
    ret,frame = camera.read()
    frame = cv2.resize(frame,(720,480))
    # MaskRCNN inference
    output_image = maskrcnn.core(model, frame, threshold=0.5, rect_th=1, text_th=1, text_size=1)
    
    cv2.imshow('Mask RCNN Output:',output_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
