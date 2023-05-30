import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
ap.add_argument("-a", "--integer_arg1", type=int, required=True,
                help="your first integer argument")
ap.add_argument("-b", "--integer_arg2", type=int, required=True,
                help="your second integer argument")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
desired_width = args["integer_arg1"]
desired_height = args["integer_arg2"]
resized_image = cv2.resize(image, (desired_width, desired_height))

cv2.imwrite('./public/resize/' + args["string_arg"]+'.jpg', resized_image)
