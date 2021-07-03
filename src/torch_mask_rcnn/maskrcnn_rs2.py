import torch
import torchvision
from PIL import Image
from torchvision import transforms as T
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import node_config as NC



COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def get_prediction(model,img, threshold):
	transform = T.Compose([T.ToTensor()])
	img = transform(img)
	model.cuda()
	img = img.cuda()
	pred = None
	pred = model([img])
	pred_score = list(pred[0]['scores'].detach().cpu().numpy())
	x = [pred_score.index(x) for x in pred_score if x > threshold]
	# Check whether detection result is empty
	if(len(x)>0):
		pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
		masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
		pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cpu().numpy())]
		pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
		masks = masks[:pred_t+1]
		pred_boxes = pred_boxes[:pred_t+1]
		pred_class = pred_class[:pred_t+1]
	else:
		masks = None
		pred_boxes = None
		pred_class = None
	return masks, pred_boxes, pred_class

def random_colour_masks(image):
	colours = [[0, 255, 0],[0, 0, 255],[255, 0, 0],[0, 255, 255],
				[255, 255, 0],[255, 0, 255],[80, 70, 180],
				[250, 80, 190],[245, 145, 50],[70, 150, 250],
				[50, 190, 190]]
	r = np.zeros_like(image).astype(np.uint8)
	g = np.zeros_like(image).astype(np.uint8)
	b = np.zeros_like(image).astype(np.uint8)
	r[image == 1], g[image == 1], b[image == 1] = colours[random.randrange(0, 10)]
	coloured_mask = np.stack([r, g, b], axis=2)
	return coloured_mask

def core(model, img_path, threshold=0.7, rect_th=3, text_size=3, text_th=3):
	# Source depends on detect mode
	if(NC.detect_mode == 0):
		img = cv2.imread('/home/xavier/vincent-dev/xavier_navigation/src/torch_mask_rcnn/data/people.jpg')
	else:
		img = img_path

	# Inference
	masks, boxes, pred_cls = get_prediction(model, img, threshold)

	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	if(masks is not None):
		for i in range(len(masks)):
			rgb_mask = random_colour_masks(masks[i])
			img = cv2.addWeighted(img, 1, rgb_mask, 0.5, 0)
			cv2.rectangle(img, boxes[i][0], boxes[i][1], color=(0, 0,255), thickness=rect_th)
			cv2.putText(img, pred_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), 		
			thickness=text_th)
	return img
