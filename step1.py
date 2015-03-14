# Visual Interfaces Spring 2015 Assignment 1
# Roberto Amorim - rja2139

import cv2
import numpy as np
from operator import itemgetter


#
def positive(value):
    if value < 0:
        return -1 * value
    else:
        return value


#
def comparehist(hist1, hist2):
    total_distance = 0
    for i in range (0, len(hist1)):
        for j in range (0, len(hist1[i])):
            for k in range (0, len(hist1[i][j])):
                total_distance += positive(hist1[i][j][k] - hist2[i][j][k])
    return total_distance / 30


for i in range(1, 41):
    results = []
    # We load the base image, against which other images will be tested
    base = cv2.imread("i" + str(i) + ".ppm")
    histbase = cv2.calcHist(base, [0, 1, 2], None, [8, 8, 8], [10, 256, 10, 256, 10, 256])
    cv2.normalize(histbase, histbase, 0, 255, cv2.NORM_MINMAX)
    mergedbase = histbase.flatten()
    for j in range(1, 41):
        test = cv2.imread("i" + str(j) + ".ppm")
        histtest = cv2.calcHist(test, [0, 1, 2], None, [8, 8, 8], [10, 256, 10, 256, 10, 256])
        cv2.normalize(histtest, histtest, 0, 255, cv2.NORM_MINMAX)
        mergedtest = histtest.flatten()
        results.append(comparehist(histbase, histtest))
    npresults = np.array(results)
    cv2.normalize(npresults, npresults, 0, 1, cv2.NORM_MINMAX)
    np.set_printoptions(suppress=True)
    for j in range (0, len(npresults)):
        results[j] = (1 - npresults[j], j + 1)
    sort = sorted(results, key=itemgetter(0))

    print sort
