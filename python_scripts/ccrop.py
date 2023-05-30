import cv2
import numpy as np
import argparse
from PIL import Image, ImageDraw
import os

circle_center = None
circle_radius = None
drawing = False
button_down = False
image = None
image_copy = None
flag = 0

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
args = vars(ap.parse_args())


def draw_circle(event, x, y, flags, param):
    global circle_center, circle_radius, drawing, button_down, image, image_copy, flag
    if event == cv2.EVENT_LBUTTONDOWN:
        circle_center = (x, y)
        drawing = True
        button_down = True
    elif button_down and event == cv2.EVENT_MOUSEMOVE:
        image = image_copy.copy()
        circle_radius = int(
            np.sqrt((x - circle_center[0])**2 + (y - circle_center[1])**2))
        cv2.circle(image, circle_center, circle_radius, (255, 255, 255), 1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        flag = 1
        button_down = False
        circle_radius = int(
            np.sqrt((x - circle_center[0])**2 + (y - circle_center[1])**2))
        cv2.circle(image, circle_center, circle_radius, (0, 0, 0), 2)


image = cv2.imread(args["image"])
image_copy = image.copy()
ogImage = image.copy()

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_circle)

while True:
    cv2.imshow('Image', image)
    key = cv2.waitKey(1) & 0xFF
    if flag == 1:
        break

# image = ogImage.copy()
mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.circle(mask, circle_center, circle_radius, 255, -1)
masked_image = cv2.bitwise_and(image, image, mask=mask)
x, y, w, h = cv2.boundingRect(mask)
cropped_image = masked_image[y:y+h, x:x+w]
cropped_mask = np.zeros(cropped_image.shape[:2], dtype=np.uint8)
cv2.circle(cropped_mask, (w//2, h//2), min(w, h)//2, 255, -1)
final_image = cv2.bitwise_and(cropped_image, cropped_image, mask=cropped_mask)
cv2.imwrite("./python_scripts/"+args["string_arg"]+'.jpg', final_image)

image = Image.open("./python_scripts/"+args["string_arg"]+'.jpg')
image = image.convert("RGBA")
width, height = image.size
mask = Image.new("L", (width, height), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((0, 0, width, height), fill=255)
result = Image.new("RGBA", (width, height))
result.paste(image, (0, 0), mask=mask)
bbox = mask.getbbox()
result = result.crop(bbox)
size = (max(width, height), max(width, height))
background = Image.new("RGBA", size, (255, 255, 255, 0))
x = (size[0] - result.width) // 2
y = (size[1] - result.height) // 2
background.paste(result, (x, y))
bbox = background.getbbox()
background = background.crop(bbox)

background.save(os.path.join("./public/ccrop", args["string_arg"]+'.png'))
os.rename("./public/ccrop/"+args["string_arg"]+'.png',
          "./public/ccrop/"+args["string_arg"]+'.jpg')
os.remove("./python_scripts/"+args["string_arg"]+'.jpg')

cv2.destroyAllWindows()
