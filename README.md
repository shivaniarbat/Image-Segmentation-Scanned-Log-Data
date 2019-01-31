# Image-Segmentation-Scanned-Log-Data

##Folder Organization : *

Input files :  ./Test_Results/approach2_testresults/input/
Input files are the input images for the program

Output: ./Test_Results/approach2_testresults/labels/
Output will be created with the name ‘test_round_<data-time-stamp>.jpg in above folder

Ground Truth Labels: ./Test_Results/approach2_testresults/ground_truth_labels/
This folder contains the ground truth labels for the respective images. Mapping can be identified by the name.

Histograms : ./Test_Results/approach2_testresults/histogram/
Histograms to show the global threshold saved as jpg file in this folder

Contours : ./Test_Results/approach2_testresults/contours/
Contours - intermediate output will be saved in this folder 

###— Instructions to run the program. **

1. Provide the input file name in the ‘approach2_image_segmentation.py’ file and run the code. 
2. Output will be generated as mentioned above. 
