# Image to Braille ASCII Art Generator

A generator that creates ASCII versions of the input image, made up of braille characters. Meant to be used in terminals/CLIs and is designed as such, but the output ASCII string can be pasted anywhere you can put text in.

## How It Works

Currently, it converts the image into black and white using based on some threshold, such that each pixel is either black or white.
From there, it loops through the image in groups of 2x4 pixels (⣿) to determine which braille characters should represent this 2x4 pixel group.

## TODOs

- Create an UI using Textual
- Add dithering option to create the illusion of shading
- Add the option to create color ASCII art