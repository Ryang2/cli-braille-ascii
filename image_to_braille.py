import cv2 # OpenCV Image Processing Library
import numpy as np
import argparse
from os import path

MAX_THRESHOLD_VALUE = 255
BRAILLE_COL = 4
BRAILLE_ROW = 2

def get_average(image: np.ndarray, h: int, w: int) -> int:
    # Return the average luminosity value
    sum = 0
    for y in range(h):
        for x in range(w):
            sum += image[y][x]
    return sum / (h * w)

def get_braille_char(pixel_group: np.ndarray) -> str:
    """
    Iterate all 8 pixels in the group, adding the corresponding value (in base 16)
      if it's filled in to calculate the final value:
    1  8
    2  10
    4  20
    40 80
    Unicode for braille char (in base 16) = U+2800 + sum
    https://en.wikipedia.org/wiki/Braille_Patterns
    """
    BRAILLE_HEX_VAL = [[0x1, 0x8], [0x2, 0x10], [0x4, 0x20], [0x40, 0x80]]
    sum = 0x0
    for y in range(BRAILLE_COL):
        for x in range(BRAILLE_ROW):
            if pixel_group[y][x] == MAX_THRESHOLD_VALUE:
                sum += BRAILLE_HEX_VAL[y][x]
    if sum == 0x0: sum = 0x1
    return chr(0x2800 + sum)

def resize(image: np.ndarray, width_in_char: int):
    # Resizes the image such that each row in the resulting ASCII string has width_in_char characters
    if width_in_char < 0: width_in_char = 80
    new_width = 2 * width_in_char
    height, width = image.shape
    new_height = int(new_width * height / width)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

'''
Inputs:
image_path: path to the input image, read by the f(n)
width_in_char: resizes the resulting string to have width_in_char characters per row
style: how the ASCII string is generated:
  - avg_thresh: calculates the average luminosity value to use as global threshold
  - adapt_thresh: calculates the local threshold of each pixel using its neighbors
invert: if True, inverts the colors before generating the ASCII string

Returns:
The ASCII string on success, or None on error
'''
def image_to_braille(image_path: str, width_in_char=None, style="avg_thresh", invert=False):
    # Read in grayscale to focus on luminosity, can try w/ color later
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Unable to read image from path: {image_path}")
        return None
    
    # Resize image if width_in_char is specified
    if width_in_char: image = resize(image, width_in_char)
    h, w = image.shape

    # For each value, if it's smaller than the threshold, it's set to 0, else 255
    thresholding_type = cv2.THRESH_BINARY
    if invert: thresholding_type = cv2.THRESH_BINARY_INV
    if style == "avg_thresh":
        threshold = get_average(image, h, w)
        _, contrast_image = cv2.threshold(image, threshold, MAX_THRESHOLD_VALUE, thresholding_type)
    elif style == "adapt_thresh":
        contrast_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholding_type, 15, 3)
    else:
        print(f"{style} is not a valid style.")
        return None
    
    # Build the output string
    output = ""
    for y in range(0, h, BRAILLE_COL):
        for x in range(0, w, BRAILLE_ROW):
            pixel_group = contrast_image[y:y+BRAILLE_COL, x:x+BRAILLE_ROW]
            output += get_braille_char(pixel_group)
        output += "\n"
    return output

def main():
    parser = argparse.ArgumentParser(description="Image to Braille ASCII Art Generator")
    parser.add_argument("image", help="The path of the input file")
    parser.add_argument("-w", "--width", metavar='80', type=int,
                        help="[Optional] The width in number of characters to resize", default=None)
    # TODO, use numbers to represent style in args?
    parser.add_argument("-s", "--style", metavar='avg_thresh', type=str,
                        help="[Optional] The rendering style, either 'avg_thresh' or 'adapt_thresh'", default="avg_thresh") 
    parser.add_argument("-i", "--invert", action="store_true",
                        help="[Optional] Invert black to white and vice versa before rendering", default=False)
    parser.add_argument("-o", "--output", action="store_true",
                        help="[Optional] Save the output in a txt file in addition to printing on the console", default=False)
    args = parser.parse_args()

    try:
        output = image_to_braille(args.image, args.width, args.style, args.invert)
        if output: print(output)
        if args.output:
            with open("result.txt", "w", encoding="utf-8") as file:
                file.write(output)
                print("Saved to result.txt!")
    except Exception as e:
        print("Error when running image_to_braille:", type(e), e)

if __name__ == "__main__":
    main()