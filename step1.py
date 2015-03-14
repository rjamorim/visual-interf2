# Visual Interfaces Spring 2015 Assignment 1
# Roberto Amorim - rja2139

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
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
    # As mentioned in https://piazza.com/class/i51cy8jip6425j?cid=95
    res = total_distance / 2 / (len(hist1) ^ 3)
    return res


#
def plot(results):
    x = 20
    fnt = ImageFont.truetype('calibrib.ttf', 18)
    plot = Image.new('RGBA', (740, 140), (200, 200, 200, 255))
    txt = Image.new('RGBA', plot.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    photo = Image.open("i" + str(results[0]) + ".ppm")
    plot.paste(photo, (x, 20))
    draw.text((x+10,90), "i" + str(results[0]) + ".ppm", font=fnt, fill=(0,0,0,255))
    for i in range (1, len(results)):
        x += 100
        photo = Image.open("i" + str(results[i][1]) + ".ppm")
        plot.paste(photo, (x, 20))
        draw.text((x+10, 90), "i" + str(results[i][1]) + ".ppm", font=fnt, fill=(0, 0, 0, 255))
        draw.text((x+10, 110), "{0:.4f}".format(results[i][0]), font=fnt, fill=(0, 0, 0, 255))
    plot = Image.alpha_composite(plot, txt)
    plot.save("color_results_" + str(results[0]) + ".png")

    print "Drew plot: " + str(results[0])


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
        #results.append(cv2.compareHist(mergedbase,mergedtest,2))
        results.append(comparehist(histbase, histtest))
    npresults = np.array(results)
    cv2.normalize(npresults, npresults, 0, 1, cv2.NORM_MINMAX)
    #np.set_printoptions(suppress=True)
    for j in range (0, len(npresults)):
        results[j] = (1 - npresults[j], j + 1)
    sort = sorted(results, key=itemgetter(0))

    print sort

    # here we mount an array with the image indexes in 7 positions:
    # the base, the three most similar and the three least similar
    result = [i, sort[38], sort[37], sort[36], sort[2], sort[1], sort[0]]
    print result

    plot(result)