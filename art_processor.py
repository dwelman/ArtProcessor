import sys
import os
from PIL import Image

def main(argv):
    if len(argv) < 2:
        print(
            '''
            Usage: This is a program to process scanned in artworks. It can be used as follows:
                arg 1: The file you wish to process
                arg 2: The name of the artwork
                arg 3: The path to where the processed files should be saved (if none are provided, it will use the current directory)

            It will save the following:
                * Original in png and jpeg
                * Original downscaled by a factor of 4 in png and jpeg
                * Original rotated 90 degrees counter-clockwise in png and jpeg
                * Orignal rotated and downscaled in png and jpeg
            All these files will be saved to their own directory, in the directory provided
            ''')
        exit(-1)
    
    # Load the image
    input_image = Image.open(argv[0])
    if input_image == None:
        print('File {} could not be opened'.format(argv[0]))
        exit(-1)

    print('Image loaded')

    output_path = '.'

    if len(argv) >= 3:
        output_path = argv[2]

    artwork_name =  argv[1]
    output_dir = '{}/{}'.format(output_path, artwork_name)
    # Create a folder in the output directory if it does not exist already
    try:
        os.mkdir(output_dir)
    except OSError:
        print('Failed to create output directory {}'.format(output_dir))
        exit(-1)

    # Create the various outputs I want
    # Save original as is, in both png and jpeg
    print('Saving originals')
    input_image.save('{}/{}-orig.png'.format(output_dir, artwork_name))
    input_image.save('{}/{}-orig.jpeg'.format(output_dir, artwork_name))

    # Downscale the image, save to png and jpeg
    print('Saving downscaled originals')
    downscale_out = input_image.resize(tuple(round(i / 4) for i in input_image.size))
    downscale_out.save('{}/{}-orig-downscaled.png'.format(output_dir, artwork_name))
    downscale_out.save('{}/{}-orig-downscaled.jpeg'.format(output_dir, artwork_name))

    # Rotate the image to the left, save to png and jpeg
    print('Saving rotated originals')
    rotated_out = input_image.rotate(90, expand=True)
    rotated_out.save('{}/{}-rot.png'.format(output_dir, artwork_name))
    rotated_out.save('{}/{}-rot.jpeg'.format(output_dir, artwork_name))

    # Finally, rotate the downscaled images
    print('Saving rotated downscaled originals')
    rotated_out = downscale_out.rotate(90, expand=True)
    rotated_out.save('{}/{}-rot-downscaled.png'.format(output_dir, artwork_name))
    rotated_out.save('{}/{}-rot-downscaled.jpeg'.format(output_dir, artwork_name))

    print('Finished processing, output can be found in {}'.format(output_dir))


if __name__ == "__main__":
   main(sys.argv[1:])