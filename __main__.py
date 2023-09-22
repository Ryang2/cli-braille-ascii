from image_to_braille import image_to_braille

PATH = "C:/Users/rickr/eclipse-workspace/cli-braille-ascii/example-256px.png"

def main():
    image = image_to_braille(PATH)
    print(image)

if __name__ == "__main__":
    main()