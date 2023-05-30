import cv2
import numpy as np
import argparse

refPt = []
blur_radius = 10
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
args = vars(ap.parse_args())


def apply_gaussian_blur(image, x, y):

    neighborhood = image[max(y-blur_radius, 0):min(y+blur_radius, image.shape[0]),
                         max(x-blur_radius, 0):min(x+blur_radius, image.shape[1])]
    blurred_neighborhood = cv2.GaussianBlur(
        neighborhood, (blur_radius*2+1, blur_radius*2+1), 0)
    image[max(y-blur_radius, 0):min(y+blur_radius, image.shape[0]),
          max(x-blur_radius, 0):min(x+blur_radius, image.shape[1])] = blurred_neighborhood


image = cv2.imread(args["image"])
cv2.namedWindow('Image')


def mouse_callback(event, x, y, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags == cv2.EVENT_FLAG_LBUTTON:
            apply_gaussian_blur(image, x, y)
            cv2.imshow('Image', image)


cv2.setMouseCallback('Image', mouse_callback)
while True:
    cv2.imshow('Image', image)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        cv2.imwrite('./public/blur/' + args["string_arg"]+'.jpg', image)
        break

cv2.destroyAllWindows()
