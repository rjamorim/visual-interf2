# Visual Interfaces Spring 2015 Assignment 1 - Step 2
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
        total_distance += positive(hist1[i] - hist2[i])
    # As mentioned in https://piazza.com/class/i51cy8jip6425j?cid=95
    res = total_distance / 2 * (89 * 60)
    return res


# Function that plots graphs ready to be included in the report containing the base image,
# the three most similar images and the three most different images
def plot(results):
    x = 20
    fnt = ImageFont.truetype('calibrib.ttf', 18)
    plot = Image.new('RGBA', (740, 120), (200, 200, 200, 255))
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
    plot = Image.alpha_composite(plot, txt)
    plot.save("texture_results_" + str(results[0]) + ".png")

    print "Drew plot: " + str(results[0])


# The function that generates a laplacian image
def laplacian(im):
    w, h = im.size
    image = np.array(im, dtype='int32')
    laplace = [[0 for i in range(w)] for j in range(h)]
    # First we deal with all the pixels that are not in the edge
    for i in range(1, h-2):
        for j in range(1, w-2):
            upper_row = image[i-1][j-1] + image[i-1][j] + image[i-1][j+1]
            middle_row = image[i][j-1] + image[i][j+1]
            lower_row = image[i+1][j-1] + image[i+1][j] + image[i+1][j+1]
            laplace[i][j] = (image[i][j] * 8) - upper_row - middle_row - lower_row
    # We worked on the center of the image, now we must work on the borders
    for j in range(1, w-1):
        middle_row = image[0][j-1] + image[0][j+1]
        lower_row = image[1][j-1] + image[1][j] + image[1][j+1]
        laplace[0][j] = (image[0][j] * 5) - middle_row - lower_row
        upper_row = image[h-2][j-1] + image[h-2][j] + image[h-2][j+1]
        middle_row = image[h-1][j-1] + image[h-1][j+1]
        laplace[h-1][j] = (image[h-1][j] * 5) - upper_row - middle_row
    for i in range(1, h-1):
        upper_row = image[i-1][0] + image[i-1][1]
        middle_row = image[i][1]
        lower_row = image[i+1][0] + image[i+1][1]
        laplace[i][j] = (image[i][j] * 5) - upper_row - middle_row - lower_row
        upper_row = image[i-1][w-2] + image[i-1][w-1]
        middle_row = image[i][w-1]
        lower_row = image[i+1][w-2] + image[i+1][w-1]
        laplace[i][j] = (image[i][j] * 5) - upper_row - middle_row - lower_row
    # And now the corners
    laplace[0][0] = (image[0][0] * 3) - image[0][1] - image[1][0] - image[1][1]
    laplace[0][w-1] = (image[0][w-1] * 3) - image[0][w-2] - image[1][w-2] - image[1][w-1]
    laplace[h-1][0] = (image[h-1][0] * 3) - image[h-1][1] - image[h-2][0] - image[h-2][1]
    laplace[h-1][w-1] = (image[h-1][w-1] * 3) - image[h-1][w-2] - image[h-2][w-2] - image[h-2][w-1]

    res = np.array(laplace)
    # The pixels end up in the range [-255, 255]. So we normalize the values to stay in the range [0, 255]
    cv2.normalize(res, res, 0, 255, cv2.NORM_MINMAX)
    return res


bins = 16
ddepth = cv2.CV_16S
for i in range(1, 41):
    results = []
    # We load the base image, against which other images will be tested
    base = cv2.imread("i" + str(i) + ".ppm")
    # Now the image gets converted for grayscale
    graybase = cv2.cvtColor(base, cv2.COLOR_RGB2GRAY)
    # Now we generate the laplacian of the image
    baselapl = laplacian(graybase)
    # And finally, the histogram is generated.
    histbase = cv2.calcHist(baselapl, [0], None, [bins], [0, 255])
    for j in range(1, 41):
        test = cv2.imread("i" + str(j) + ".ppm")
        graytest = cv2.cvtColor(test, cv2.COLOR_RGB2GRAY)
        testlapl = cv2.Laplacian(graytest, ddepth, 1, scale = 1,delta = 0)
        testlapl = cv2.convertScaleAbs(testlapl)
        histtest = cv2.calcHist(testlapl, [0], None, [bins], [0, 255])
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
    result = [i, sort[38], sort[37], sort[36], sort[0], sort[1], sort[2]]

    plot(result)