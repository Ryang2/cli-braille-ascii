# Image to Braille ASCII Art Generator

A generator that creates ASCII versions of the input image, made up of braille characters. Meant to be used in terminals/CLIs and is designed as such, but the output ASCII string can be pasted anywhere you can put text in.

![Example](https://raw.githubusercontent.com/Ryang2/cli-braille-ascii/main/images/example-screenshot.jpg)

## To Run:

**The CLI:**

Install dependencies with pipenv then run:

`image_to_braille.py [path-of-image] [-w width-in-chars] [-s style] [-i] [-o name-of-file]`

Optional arguments:
- width: resizes the resulting ASCII with number of characters per row equaling the width
- style: changes how the threshold is calculated (default is Average Threshold)
- invert: inverts black and white before generating the ASCII
- output: outputs the resulting ASCII in <name-of-file>.txt instead of printing on the console

The help (-h) option will also display the above options.

**Using the UI Wrapper:**

Install dependencies with pipenv then run:

`textual run --dev main.py`

Enter the arguments on the sidebar and press "generate" for the image.

## How It Works

Currently, it converts the image into black and white using based on some threshold, such that each pixel is either black or white.
From there, it loops through the image in groups of 2x4 pixels (⣿) to determine which braille characters should represent this 2x4 pixel group.

## Future Improvements

- Add dithering option to create the illusion of shading
- Add the option to create color ASCII art

## Other Notes

Sample image generated with https://playgroundai.com/