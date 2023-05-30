import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
args = vars(ap.parse_args())

selected_color = None


def select_color(event, x, y, flags, param):
    global selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_color = image[y, x]
        cv2.destroyAllWindows()


def select_color_from_image():
    global image

    image = cv2.imread(args["image"])
    cv2.namedWindow('Select Color')
    cv2.setMouseCallback('Select Color', select_color)
    cv2.imshow('Select Color', image)
    cv2.waitKey(0)

    return selected_color


def rgb_to_hex(rgb):
    hex_value = '#{:02x}{:02x}{:02x}'.format(rgb[2], rgb[1], rgb[0])
    return hex_value


selected_color = select_color_from_image()
hex = rgb_to_hex(selected_color)
selected_color = selected_color[::-1]
print('RGB values: ', selected_color, " Hex-value: ", hex)
