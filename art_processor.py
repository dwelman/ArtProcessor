import sys
import os
from PIL import Image

def main(argv):
    if len(argv) < 2:
        print(
            '''
            Usage: This is a program to process scanned in artworks. It can be used as follows:
                arg 1: The folder you wish to process
                arg 2: The name of the artwork
                arg 3: The path to where the processed files should be saved (if none are provided, it will use the current directory)

            It will save the following:
                * Original in png and jpeg
                * Original downscaled by a factor of 4 in png and jpeg
                * Original rotated 90 degrees counter-clockwise in png and jpeg
                * Orignal rotated and downscaled in png and jpeg
            All these files will be saved to their own directory, in the directory provided

            Each image in the provided folder will be processed, named after the artwork provided and the number of the artwork
            ''')
        exit(-1)

    output_path = '.'

    if len(argv) >= 3:
        output_path = argv[2]

    artwork_name = argv[1]

    output_dir = '{}/{}'.format(output_path, artwork_name)
    # Create a folder in the output directory if it does not exist already
    try:
        os.mkdir(output_dir)
    except OSError:
        print('Failed to create output directory {}'.format(output_dir))
        exit(-1)

    image_index = 0
    
    # Load each image in the folder
    directory_name = argv[0]
    directory = os.fsencode(directory_name)

    image_total = len(os.listdir(directory))

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        input_image = Image.open(directory_name + os.sep + filename)

        if input_image == None:
            print('File {} could not be opened'.format(filename))
            exit(-1)

        #Save an RGB copy of the input image in-case it has any transparency
        rgb_image = input_image.convert("RGB") if input_image.mode in ('RGBA', 'P') else input_image
        
        print('Processing image {}/{}'.format(image_index + 1, image_total))

        new_filename = '{}_{}'.format(artwork_name, image_index)

        # Create the various outputs I want
        # Save original as is, in both png and jpeg
        try:
            print('Saving originals')
            input_image.save('{}/{}-orig.png'.format(output_dir, new_filename))
            rgb_image.save('{}/{}-orig.jpeg'.format(output_dir, new_filename))
        except Exception as e: print('Failed to process image: {}'.format(e)) 

        # Downscale the image, save to png and jpeg
        try:
            print('Saving downscaled originals')
            downscale_out = input_image.resize(tuple(round(i / 4) for i in input_image.size))
            downscale_out.save('{}/{}-orig-downscaled.png'.format(output_dir, new_filename))
            rgb_image.save('{}/{}-orig-downscaled.jpeg'.format(output_dir, new_filename))
        except Exception as e: print('Failed to process image: {}'.format(e))  

        # Rotate the image to the left, save to png and jpeg
        try:
            print('Saving rotated originals')
            rotated_out = input_image.rotate(90, expand=True)
            rotated_out.save('{}/{}-rot.png'.format(output_dir, new_filename))
            rgb_image.save('{}/{}-rot.jpeg'.format(output_dir, new_filename))
        except Exception as e: print('Failed to process image: {}'.format(e))  

        # Finally, rotate the downscaled images
        try:
            print('Saving rotated downscaled originals')
            rotated_out = downscale_out.rotate(90, expand=True)
            rotated_out.save('{}/{}-rot-downscaled.png'.format(output_dir, new_filename))
            rgb_image.save('{}/{}-rot-downscaled.jpeg'.format(output_dir, new_filename))
        except Exception as e: print('Failed to process image: {}'.format(e))  

        image_index += 1

    print('Finished processing, output can be found in {}'.format(output_dir))


if __name__ == "__main__":
   main(sys.argv[1:])