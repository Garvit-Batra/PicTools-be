import cv2
import argparse

start_x, start_y, end_x, end_y = 0, 0, 0, 0
cropping = False
button_down = False
image_copy = None
image = None
ogImage = None
flag = 0

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
args = vars(ap.parse_args())


def mouse_callback(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, cropping, button_down, image_copy, image, ogImage, flag
    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        cropping = True
        button_down = True
        image_copy = image.copy()
    elif button_down and event == cv2.EVENT_MOUSEMOVE:
        image = image_copy.copy()
        end_x, end_y = x, y
        cropping = True
        cv2.rectangle(image, (start_x, start_y),
                      (end_x, end_y), (255, 255, 255), 1)
    elif event == cv2.EVENT_LBUTTONUP:
        end_x, end_y = x, y
        cropping = False
        button_down = False
        crop = ogImage[start_y:end_y, start_x:end_x]
        cv2.imwrite('./public/rcrop/' + args["string_arg"]+'.jpg', crop)
        flag = 1


image = cv2.imread(args["image"])
ogImage = image

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

while True:
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF
    if flag == 1:
        break

cv2.destroyAllWindows()
