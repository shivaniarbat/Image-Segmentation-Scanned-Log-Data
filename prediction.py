import numpy as np
import glob
from PIL import Image
from matplotlib import pyplot as plt

''' to determine accuracy of the predictions '''
''' since only 10 ground truth labels are created '''

target_files = []
prediction_files = []
accuracy_arr = np.zeros((11,4))

i = 0
for fname in glob.glob("/Users/shivani/Documents/approach2_testresults/ground_truth_labels/*.jpg"):
    if i <= 10:
        target_files.append(fname)
        i = i + 1

i = 0
for fname in glob.glob("/Users/shivani/Documents/approach2_testresults/labels/*.jpg"):
    if i <= 10:
        prediction_files.append(fname)
        i = i + 1


for index in range(0,10,1):
    target_file = Image.open(target_files[index])
    pred_file =  Image.open(prediction_files[index])

    target_file_arr = np.asarray(target_file)
    pred_2D = np.asarray(pred_file)


    target_2D = np.zeros((512,512),dtype='uint8')

    for i in range(0,target_file_arr.shape[0],1):
        for j in range(0, target_file_arr.shape[1], 1):
            temp = 0
            for k in range(0, target_file_arr.shape[2], 1):
                temp = temp + target_file_arr[i][j][k]
            target_2D[i][j] = temp / 3

    target = target_2D < 254
    prediction = pred_2D < 254

    TP = 0
    TN = 0
    FP = 0
    FN = 0

    for i in range(0,512,1):
        for j in range(0,512,1):
            if target[i][j] == True and prediction[i][j] == True: TP = TP + 1

            if target[i][j] == False and prediction[i][j] == False: TN = TN + 1

            if target[i][j] == True and prediction[i][j] == False: FN = FN + 1

            if target[i][j] == False and prediction[i][j] == True: FN = FN + 1

    accuracy = (TP + TN )/(TP+TN+FP+FN)
    print(accuracy)
    accuracy_arr[index + 1] = accuracy

plt.plot(accuracy_arr)
plt.xlabel('samples')
plt.ylabel('accuracy')
plt.show()

