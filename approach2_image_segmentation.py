import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from skimage.filters import threshold_otsu
import math
from skimage import measure
import imageio
import datetime
datetime_val = str(datetime.datetime.now())
test_round = datetime_val     # enter the test round number or current-data-time will be appended in the output file name

''' Enter the input file name '''
input_file_name = "/Users/shivani/Documents/approach2_testresults/input/test-round-17.jpg"
ct_scan_bed_threshold = 315 # enter the position of ct_scan bed in x-axis to remove the data

''' filename to store the test results and identify the repsective output'''
filename = 'test-round-'+ str(test_round)

''' open the input image file '''
image = Image.open(input_file_name)

# reshape the input image in 512 X 512 format
img_array = np.reshape(list(image.getdata()),(512,512))

# apply global threshold to the image ; global_thresh will hold the threshold value selected globally
global_thresh = threshold_otsu(img_array)
binary_global = image > global_thresh

#plot histogram to display the thresholded value
plt.bar(range(len(image.histogram())),image.histogram())    # original histogram
plt.axvline(global_thresh,color='r')

#save the histomgram for the respective test round
plt.savefig("/Users/shivani/Documents/approach2_testresults/histograms/"+filename+".jpg")
plt.show()

''' heuristics to determine if we need to grow the region :- 
if atleast 7 neighbors are of same colour change to that color; the image is binary since its thresholded
'''

''' function to determine the eight neighbours of the pixel in the image '''
def eight_neighbourhoodlist_function(array,x,y):
    eight_neighbourhoodlist = []
    if x+1 <= 511 and y+1 <= 511 and y-1 >= 0 and x-1 >=0:
        eight_neighbourhoodlist = [array[x, y - 1],array[x-1,y-1],array[x-1,y],array[x-1,y+1],array[x,y+1],array[x+1,y+1],array[x+1,y],array[x+1,y-1]]
        return eight_neighbourhoodlist
    return eight_neighbourhoodlist

''' remove pixels which does not belong to any significant reigion '''
for i in range(0,512,1):
    for j in range(0,512,1):
        list = eight_neighbourhoodlist_function(binary_global,i,j)
        if list.count(True) >= 7: binary_global[i][j] = True
        if list.count(False) >= 7: binary_global[i][j] = False

thresholded_image_array = np.zeros((512,512),dtype='uint8')

''' remove the CT scan bed data '''
''' this data is not removed earlier as it would have affected the global threshold value'''

for i in range(0,512,1):
    for j in range(0,512,1):
        if binary_global[i][j] == True: thresholded_image_array[i][j] = 255

        if i >= ct_scan_bed_threshold : thresholded_image_array[i][j] = 0

contours = measure.find_contours(thresholded_image_array,0.1)

fig, ax = plt.subplots()
ax.imshow(thresholded_image_array, interpolation='nearest', cmap=plt.cm.gray)

''' plot the contours for the threhsolded images '''
for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=1)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

final_image = np.full((512,512),fill_value=255,dtype='uint8')

print(len(contours[1]))

for n, contour in enumerate(contours):
    var = contours[n][1][1]

    for contour_count in range(0,n,1):
        for pts in range(0,len(contours[contour_count]),1):
            point = contours[contour_count][pts]
            x = math.ceil(point[0])
            y = math.ceil(point[1])
            final_image[x][y] = 0
            x = math.floor(point[0])
            y = math.floor(point[1])
            final_image[x][y] = 0

plt.imshow(final_image,cmap='gray')
plt.show()

''' contours generated in above steps determine the areas around different regions. Below we fill the regions inside the 
contours '''

count = 0
while True:
    try:
        final_image_old = final_image
        temp_image = np.copy(final_image_old)
        count = count + 1
        for i in range(0,512,1):
            for j in range(0,512,1):
                if final_image[i][j] == 255:
                    if i - 1 >= 0 and j - 1 >= 0 and i + 1 < 512 and j + 1 < 512:
                        fourNeighbor = [int(final_image[i - 1][j]), int(final_image[i][j + 1]),
                                        int(final_image[i + 1][j]), int(final_image[i][j - 1])]
                        if fourNeighbor.count(0) >= 3 :
                            final_image[i][j] = 0

        if np.array_equal(temp_image,final_image):
            break

    except:
        if np.array_equal(temp_image,final_image):
            break

''' plot the final image '''
plt.imshow(final_image,cmap='gray')
plt.show()

''' save the output of the above procedures which determined the contours and labels '''

fig.savefig("/Users/shivani/Documents/approach2_testresults/contours/"+filename+".jpg")
imageio.imwrite("/Users/shivani/Documents/approach2_testresults/labels/"+filename+".jpg",final_image)

# end of code