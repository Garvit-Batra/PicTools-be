# Concept is to first convert the RGB into LAB image
# then passing L channel of LAB to the trained model and getting a AB out of it
# Using this AB(result of forward pass) we will combine it with the L channel(input)
# then again we get LAB image and then convert to RGB and it's done

# Credits:
# 	1. https://github.com/opencv/opencv/blob/master/samples/dnn/colorization.py
# 	2. http://richzhang.github.io/colorization/
# 	3. https://github.com/richzhang/colorization/

import numpy as np
import argparse
import cv2

model_part1 = "./model/colorization_release_v2_part1.caffemodel"
model_part2 = "./model/colorization_release_v2_part2.caffemodel"
model_part3 = "./model/colorization_release_v2_part3.caffemodel"
combined_model = "./model/colorization_release_v2_combined.caffemodel"

with open(model_part1, 'rb') as f:
    data_part1 = f.read()
with open(model_part2, 'rb') as f:
    data_part2 = f.read()
with open(model_part3, 'rb') as f:
    data_part3 = f.read()
combined_data = data_part1 + data_part2 + data_part3
with open(combined_model, 'wb') as f:
    f.write(combined_data)

PROTOTXT = "./model/colorization_deploy_v2.prototxt.txt"
POINTS = "./model/pts_in_hull.npy"
MODEL = combined_model

print("Starting")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
args = vars(ap.parse_args())

net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)

print("Manipulating layers")
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

image = cv2.imread(args["image"])
scaled = image.astype("float32") / 255.0
lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

resized = cv2.resize(lab, (224, 224))
L = cv2.split(resized)[0]
L -= 50

print("Filling")
net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

L = cv2.split(lab)[0]
colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
colorized = np.clip(colorized, 0, 1)
colorized = (255 * colorized).astype("uint8")

print("Ending")
cv2.imwrite('./public/colored/' + args["string_arg"]+'.jpg', colorized)
