from PIL import Image
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
ap.add_argument("-s", "--string_arg", type=str, required=False,
                help="your string argument")
ap.add_argument("-a", "--integer_arg1", type=int, required=True,
                help="your first integer argument")
args = vars(ap.parse_args())

image = Image.open(args["image"])
target_file_size_kb = args["integer_arg1"]

quality = 99
max_quality = 100
min_quality = 1

# add if-else if input_quality > original_quality


while True:

    image.save("./python_scripts/" +
               args["string_arg"]+'.jpg', optimize=True, quality=quality)
    file_size_kb = os.path.getsize(
        "./python_scripts/"+args["string_arg"]+'.jpg') / 1024
    if file_size_kb <= target_file_size_kb or quality <= min_quality or quality >= max_quality:
        image.save("./public/compress/" +
                   args["string_arg"]+'.jpg', optimize=True, quality=quality)
        break
    if file_size_kb > target_file_size_kb:
        max_quality = quality
        quality = int((quality + min_quality) / 2)
    else:
        min_quality = quality
        quality = int((quality + max_quality) / 2)

os.remove("./python_scripts/"+args["string_arg"]+'.jpg')
