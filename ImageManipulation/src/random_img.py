#!/usr/bin/env python

"""
    Created by cengen on 2/18/18.
"""

import numpy
from PIL import Image
from scipy.signal import convolve2d
from scipy.ndimage import imread
from scipy import ndimage
from scipy.misc import imsave
from scipy import misc
import cProfile


def sobel_filter(img):
    im = imread(img)
    im = im.astype('int32')
    dx = ndimage.sobel(im, 0)  # horizontal derivative
    dy = ndimage.sobel(im, 1)  # vertical derivative
    mag = numpy.hypot(dx, dy)  # magnitude
    mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)

    return mag


def main():

    array = numpy.random.randint(0, 255, (1080 // 2, 1920 // 2, 3)).astype("uint8")

    img1 = Image.fromarray(array, 'RGB')
    img1.save('./images/random.png')

    img1 = './images/random.png'
    img1 = sobel_filter(img1)

    img2 = "./images/goats.jpg"

    img2 = sobel_filter(img2)

    img3 = "./images/cat_goat.jpg"

    img3 = sobel_filter(img3)

    misc.imshow(img1)
    misc.imshow(img2)
    misc.imshow(img3)


if __name__ == "__main__":
    #cProfile.run("main()")
    main()
