# Built in packages
import math
import sys

# Matplotlib will need to be installed if it isn't already. This is the only package allowed for this base part of the 
# assignment.
from matplotlib import pyplot
from matplotlib.patches import Rectangle

# import our basic, light-weight png reader library
import imageIO.png

# Define constant and global variables
TEST_MODE = False    # Please, DO NOT change this variable!

def readRGBImageToSeparatePixelArrays(input_filename):
    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):
    new_pixel_array = []
    for _ in range(image_height):
        new_row = []
        for _ in range(image_width):
            new_row.append(initValue)
        new_pixel_array.append(new_row)

    return new_pixel_array


###########################################
### You can add your own functions here ###
###########################################

def newGreyscale(image_width, image_height):
    return [[0 for _ in range(image_width)] for _ in range(image_height)]

def convertToGreyscale(image_width, image_height, px_array_r, px_array_g, px_array_b):
    out = newGreyscale(image_width, image_height)
    for row in range(image_height):
        for col in range(image_width):
            out[row][col] =  int(0.3 * px_array_r[row][col] + 0.6 * px_array_g[row][col] + 0.1 * px_array_b[row][col])
    return out

def computeCumulativeHistogram(pixel_array, image_width, image_height, nr_bins):
    count = 0
    output = []
    for i in range(nr_bins):
        for row in range(image_height):
            for col in range(image_width):
                if (pixel_array[row][col] == i):
                    count += 1
        output.append(count)
    return output

def stretchContrast(pixel_array, image_width, image_height):
    hist = computeCumulativeHistogram(pixel_array, image_width, image_height, 256)
    five_percent = image_width * image_height * 0.05
    ninety_five_percent = image_width * image_height * 0.95
    left_boundry = 0
    right_boundry = 255
    for colour in range(256):
        if hist[colour] > five_percent:
            left_boundry = colour
            break
    for colour in reversed(range(256)):
        if hist[colour] < ninety_five_percent:
            right_boundry = colour
            break
    out = newGreyscale(image_width, image_height)
    for row in range(image_height):
        for col in range(image_width):
            new_value = (255 / (right_boundry - left_boundry)) * (pixel_array[row][col] - left_boundry)
            if new_value > 255:
                new_value = 255
            if new_value < 0:
                new_value = 0
            out[row][col] = new_value
    return out
    
def scharrFilter(pixel_array, image_width, image_height):
    horizontal_edge = newGreyscale(image_width, image_height)
    vertical_edge = newGreyscale(image_width, image_height)
    for row in range(1, image_height - 1):
        for col in range(1, image_width - 1):
            horizontal_edge[row][col] = (
                3 * pixel_array[row-1][col-1]
                + 10 * pixel_array[row][col-1]
                + 3 * pixel_array[row+1][col-1]
                - 3 * pixel_array[row-1][col+1]
                - 10 * pixel_array[row][col+1]
                - 3 * pixel_array[row+1][col+1]) / 32
            vertical_edge[row][col] = (
                3 * pixel_array[row-1][col-1]
                + 10 * pixel_array[row-1][col]
                + 3 * pixel_array[row-1][col+1]
                - 3 * pixel_array[row+1][col-1]
                - 10 * pixel_array[row+1][col]
                - 3 * pixel_array[row+1][col+1]) / 32
    return (horizontal_edge, vertical_edge)

def meanFilter(pixel_array, image_width, image_height):
    out = newGreyscale(image_width, image_height)
    for row in range(2, image_height - 2):
        for col in range(2, image_width - 2):
            sum = 0
            for row_dif in range(-2, 3):
                for col_dif in range(-2, 3):
                    sum += pixel_array[row + row_dif][col + col_dif]
            out[row][col] = sum / 25
    return out

def segment(pixel_array, image_width, image_height):
    out = newGreyscale(image_width, image_height)
    for row in range(image_height):
        for col in range(image_width):
            if pixel_array[row][col] >= 26:
                out[row][col] = 255;
    return out

def newCircularKernel():
    return [[0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0]]

def dilate(pixel_array, image_width, image_height):
    out = newGreyscale(image_width, image_height)
    kernel = newCircularKernel()
    for row in range(image_height):
        for col in range(image_width):
            include = 0
            for row_dif in range(-2, 3):
                for col_dif in range(-2, 3):
                    if (kernel[row_dif + 2][col_dif + 2] == 1) & (inRng(pixel_array, row + row_dif, col + col_dif) == 255):
                        include = 255
                        break
                if include != 0:
                    break
            out[row][col] = include
    return out

def erode(pixel_array, image_width, image_height):
    out = newGreyscale(image_width, image_height)
    kernel = newCircularKernel()
    for row in range(image_height):
        for col in range(image_width):
            include = 255
            for row_dif in range(-2, 3):
                for col_dif in range(-2, 3):
                    if (kernel[row_dif + 2][col_dif + 2] == 1) & (inRng(pixel_array, row + row_dif, col + col_dif) == 0):
                        include = 0
                        break
                if include != 255:
                    break
            out[row][col] = include
    return out
            

def inRng(pixel_array, row, col):
    try:
        return pixel_array[row][col]
    except:
        return 0

def getBoundingBoxes(pixel_array, image_width, image_height):
    out = []
    for row in range(0, image_height, 4):
        for col in range(0, image_width, 4):
            if pixel_array[row][col] == 255:
                out.append(explore(pixel_array, row, col))
    return out

def explore(pixel_array, row, col):
    row_queue = [row]
    col_queue = [col]
    pixel_array[row][col] = 0
    # [0] = min_col, [1] = min_row, [2] = max_col, [3] = max_row
    out = [col, row, col, row]
    
    while len(row_queue) > 0:
        row = row_queue.pop(0)
        col = col_queue.pop(0)

        if row < out[1]:
            out[1] = row
        if col < out[0]:
            out[0] = col
        if row > out[3]:
            out[3] = row
        if col > out[2]:
            out[2] = col

        for row_dif in range(-1, 2):
            for col_dif in range(-1, 2):
                if pixel_array[row + row_dif][col + col_dif] == 255:
                    pixel_array[row + row_dif][col + col_dif] = 0
                    row_queue.append(row + row_dif)
                    col_queue.append(col + col_dif)

    return out
    
        


# This is our code skeleton that performs the coin detection.
def main(input_path, output_path):
    # This is the default input image, you may change the 'image_name' variable to test other images.
    image_name = 'hard_case_2'
    input_filename = f'./Images/hard/{image_name}.png'
    if TEST_MODE:
        input_filename = input_path

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)
    
    ###################################
    ### STUDENT IMPLEMENTATION Here ###
    ###################################

    # Convert image to greyscale
    px_array = convertToGreyscale(image_width, image_height, px_array_r, px_array_g, px_array_b)
    # Stretch image contrast
    px_array = stretchContrast(px_array, image_width, image_height)

    (horizontal_edge, vertical_edge) = scharrFilter(px_array, image_width, image_height)

    # Take the absolute sum of the horizontal and vertical edge maps
    for row in range(image_height):
        for col in range(image_width):
            px_array[row][col] = abs(horizontal_edge[row][col]) + abs(vertical_edge[row][col])

    # Blur image
    for _ in range(3):
        px_array = meanFilter(px_array, image_width, image_height)

    # Threshold image
    px_array = segment(px_array, image_width, image_height)

    # Erode and dilate image
    for _ in range(5):
        px_array = dilate(px_array, image_width, image_height)
    for _ in range(5):
        px_array = erode(px_array, image_width, image_height)

    bounding_box_list = getBoundingBoxes(px_array, image_width, image_height)
    
    ############################################
    ### Bounding box coordinates information ###
    ### bounding_box[0] = min x
    ### bounding_box[1] = min y
    ### bounding_box[2] = max x
    ### bounding_box[3] = max y
    ############################################
    
    # bounding_box_list = [[150, 140, 200, 190]]  # This is a dummy bounding box list, please comment it out when testing your own code.
    px_array = px_array_r
    
    fig, axs = pyplot.subplots(1, 1)
    axs.imshow(px_array, aspect='equal')
    
    # Loop through all bounding boxes
    for bounding_box in bounding_box_list:
        bbox_min_x = bounding_box[0]
        bbox_min_y = bounding_box[1]
        bbox_max_x = bounding_box[2]
        bbox_max_y = bounding_box[3]
        
        bbox_xy = (bbox_min_x, bbox_min_y)
        bbox_width = bbox_max_x - bbox_min_x
        bbox_height = bbox_max_y - bbox_min_y
        rect = Rectangle(bbox_xy, bbox_width, bbox_height, linewidth=2, edgecolor='r', facecolor='none')
        axs.add_patch(rect)
        
    pyplot.axis('off')
    pyplot.tight_layout()
    default_output_path = f'./output_images/{image_name}_with_bbox.png'
    if not TEST_MODE:
        # Saving output image to the above directory
        pyplot.savefig(default_output_path, bbox_inches='tight', pad_inches=0)
      
        # Show image with bounding box on the screen
        pyplot.imshow(px_array, cmap='gray', aspect='equal')
        pyplot.show()
    else:
        # Please, DO NOT change this code block!
        pyplot.savefig(output_path, bbox_inches='tight', pad_inches=0)



if __name__ == "__main__":
    num_of_args = len(sys.argv) - 1
    
    input_path = None
    output_path = None
    if num_of_args > 0:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        TEST_MODE = True
    
    main(input_path, output_path)
    
