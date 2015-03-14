# Visual Interfaces Spring 2015 Assignment 1
# Roberto Amorim - rja2139

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from operator import itemgetter


# Function that guarantees a positive value when calculating pixel distances
def positive(value):
    if value < 0:
        return -1 * value
    else:
        return value


# L1_NORM calculation of pixel distances to evaluate the difference between two 3D histograms
def comparehist(hist1, hist2):
    total_distance = 0
    for i in range (0, len(hist1)):
        for j in range (0, len(hist1[i])):
            for k in range (0, len(hist1[i][j])):
                total_distance += positive(hist1[i][j][k] - hist2[i][j][k])
    # As mentioned in https://piazza.com/class/i51cy8jip6425j?cid=95
    res = total_distance / 2 / (89 * 60)
    return res


# Function that plots graphs ready to be included in the report containing the base image,
# the three most similar images and the three most different images
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
    # Histogram generation is done in 3D fashion (one dimension for each color channel)
    # Color range is calculated to be from intensity 10 to 255, so at to eliminate darker
    # backgrounds (in the range 0 - 9)
    histbase = cv2.calcHist(base, [0, 1, 2], None, [8, 8, 8], [10, 255, 10, 255, 10, 255])
    # The histogram gets normalized so that each value ranges from 0 to 255
    cv2.normalize(histbase, histbase, 0, 255, cv2.NORM_MINMAX)
    for j in range(1, 41):
        test = cv2.imread("i" + str(j) + ".ppm")
        histtest = cv2.calcHist(test, [0, 1, 2], None, [8, 8, 8], [10, 255, 10, 255, 10, 255])
        cv2.normalize(histtest, histtest, 0, 255, cv2.NORM_MINMAX)
        results.append(comparehist(histbase, histtest))
    npresults = np.array(results)
    # The results get normalized to a range from 0 to 1, 0 meaning total correlation and 1 meaning the
    # image most dissimilar to the base
    cv2.normalize(npresults, npresults, 0, 1, cv2.NORM_MINMAX)
    # Here the values in the results array get inverted so that 1 means total correlation and 0 means
    # the most dissimilar image. Also we add an index to the array
    for j in range (0, len(npresults)):
        results[j] = (1 - npresults[j], j + 1)
    # Now results get sorted so that most dissimilar image comes first, o=most similar comes last
    sort = sorted(results, key=itemgetter(0))

    # here we mount an array with the image indexes in 7 positions:
    # the base, the three most similar and the three least similar
    result = [i, sort[38], sort[37], sort[36], sort[2], sort[1], sort[0]]
    print result

    plot(result)