import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance

target_file = Image.open("/Users/shivani/Documents/approach2_testresults/ground_truth_labels/test1_gt.jpg")

pred_file =  Image.open("/Users/shivani/Documents/approach2_testresults/labels/test-round-1.jpg")

target_file_arr = np.asarray(target_file)
pred_2D = np.asarray(pred_file)


target_2D = np.zeros((512,512),dtype='uint8')

for i in range(0,target_file_arr.shape[0],1):
    for j in range(0, target_file_arr.shape[1], 1):
        temp = 0
        for k in range(0, target_file_arr.shape[2], 1):
            temp = temp + target_file_arr[i][j][k]
        target_2D[i][j] = temp / 3

target = target_2D > 254
prediction = pred_2D > 254

''' determine IoU score'''

intersection = np.logical_and(target, prediction)
union = np.logical_or(target, prediction)
iou_score = np.sum(intersection) / np.sum(union)

print(iou_score)
