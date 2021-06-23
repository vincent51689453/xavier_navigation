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
maskrcnn.detect_mode = 0

# Load model checkpoint
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# MaskRCNN inference
img_path = '/home/xavier/vincent-dev/navigation_ws/src/torch_mask_rcnn/data/input_img/people.jpg'
output_image = maskrcnn.core(model, img_path, threshold=0.5, rect_th=6, text_th=1, text_size=1)

# Display ouput
cv2.imshow('Output',output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()