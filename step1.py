# Visual Interfaces Spring 2015 Assignment 1
# Roberto Amorim - rja2139

import cv2
import numpy as np

results=[]

def positive(value):
    if value < 0:
        return (-1 * value)
    else:
        return value


def comparehist(hist1, hist2):
    total_distance = 0
    for r in range (0, len(hist1)):
        for g in range (0, len(hist1[r])):
            for b in range (0, len(hist1[r][g])):
                total_distance += (positive(hist1[r][g][b] - hist2[r][g][b]))
    return total_distance

#for i in range(1, 40):
i = 4
# We load the base image, against which other images will be tested
base = cv2.imread("i" + str(i) + ".ppm")

histbase = cv2.calcHist(base, [0,1,2], None, [8,8,8], [10, 256, 10, 256, 10, 256])
cv2.normalize(histbase, histbase, 0, 255, cv2.NORM_MINMAX)
for j in range(1, 41):
    #if i == j:
    #    continue
    test = cv2.imread("i" + str(j) + ".ppm")
    histtest = cv2.calcHist(test, [0,1,2], None, [8,8,8], [10, 256, 10, 256, 10, 256])
    cv2.normalize(histtest, histtest, 0, 255, cv2.NORM_MINMAX)
    results.append(comparehist(histbase,histtest))
print results
npres = np.array(results)
cv2.normalize(npres,npres,0,1,cv2.NORM_MINMAX)
    # print "Image " + str(j) + ": " + str(result)



#print result