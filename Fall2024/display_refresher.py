#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
import time
from PIL import Image,ImageDraw,ImageFont, ImageChops
import traceback

logging.basicConfig(level=logging.DEBUG)
picdir = '/home/vml/waveshare_demo/e-Paper/RaspberryPi_JetsonNano/python/pic'
libdir = '/home/vml/waveshare_demo/e-Paper/RaspberryPi_JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

# Image specifications (px)
WIDTH = 800
HEIGHT = 480
MARGIN = 15
FONT_RATIO = 0.75 # ratio of the header font to body font size
IMAGE_BMP_DIR = "/home/vml/display_imgs/"
MONOCOLOR_IMAGE = True # will search for the red and black bmp if false, only black if true
MONOCOLOR_BLACK = True  # will display the monocolor image as black if true, as red if false

# method used for testing which combines 2 binary images into one black-red image to simulate how it would appear on the e-ink display
def combine_b_r_images(black_image, red_image):
    black_img = Image.new("RGB", black_image.size, (255, 255, 255))  # Start with white background
    red_img = Image.new("RGB", red_image.size, (255, 255, 255))    # Start with white background

    black_pixels = black_img.load()
    red_pixels = red_img.load()
    
    # Apply black overlay for img1
    for y in range(black_image.size[1]):
        for x in range(black_image.size[0]):
            if not black_image.getpixel((x, y)):  # If pixel is 1 (white in binary)
                black_pixels[x, y] = (0, 0, 0)  # Set to black

    # Apply red overlay for img2
    for y in range(red_image.size[1]):
        for x in range(red_image.size[0]):
            if not red_image.getpixel((x, y)):  # If pixel is 1 (white in binary)
                red_pixels[x, y] = (255, 0, 0)  # Set to red

    combined_img = Image.new("RGB", black_image.size, (255, 255, 255))  # White background
    combined_pixels = combined_img.load()

    # Overlay black and red images, prioritizing red
    for y in range(black_image.size[1]):
        for x in range(black_image.size[0]):
            if red_pixels[x, y] == (255, 0, 0):  # Red shape
                combined_pixels[x, y] = (255, 0, 0)
            elif black_pixels[x, y] == (0, 0, 0):  # Black shape
                combined_pixels[x, y] = (0, 0, 0)
    # Show the result
    # combined_img.show()
    # combined_img.save("folder\\name.jpg") # You can use this to save images if you're having trouble saving them otherwise

# opens the python repr file saved by the scraper as a list object, outputs as rows
def read_schedule(sched_file):
    with open(sched_file, "r") as file:
        rows = eval(file.read())
    header = rows[0]
    hours = "\n".join(rows[1:])
    return header, hours

header_text, hours = read_schedule('/home/vml/Fall_2024_files/schedule.txt')

correct_size = False
big_font_size = 90
black_image = Image.new('1', (WIDTH, HEIGHT), 'white')
red_image = Image.new('1', (WIDTH, HEIGHT), 'white')
while not correct_size:
    # drawing in the margin size (uncomment for testing)
    # spacing_draw.rectangle([MARGIN, MARGIN, WIDTH-MARGIN, HEIGHT-MARGIN])
    # setting the correct size as True unless proven otherwise
    correct_size = True
    
    # Create the blank image
    black_image = Image.new('1', (WIDTH, HEIGHT), 'white')
    black_draw = ImageDraw.Draw(black_image)
    
    red_image = Image.new('1', (WIDTH, HEIGHT), 'white')
    red_draw = ImageDraw.Draw(red_image)
    
    # creating the font objects
    big_font = ImageFont.truetype(font=os.path.join(picdir, 'Font.ttc'), size=big_font_size)
    small_font_size = int(big_font_size*FONT_RATIO)
    small_font = ImageFont.truetype(font=os.path.join(picdir, 'Font.ttc'), size=small_font_size)
    
    # calculating the size of the header
    header_bbox = red_draw.textbbox((10, 10), header_text, font=big_font)
    header_width = header_bbox[2] - header_bbox [0]
    header_height = header_bbox[3] - header_bbox[1]
    # print('header:', header_height)
    
    # if the header is wider than the image-margins, it is too big
    if header_width > (WIDTH - 2 * MARGIN):
        correct_size = False
    
    # Drawing the individual lines of the header (centered)
    
    # y_offset represents the starting y-coordinate for the next drawn image, so it gets
    # incremented whenever text is made so that the next line starts at the correct height
    y_offset = MARGIN
    for line in header_text.split('\n'):
        line_bbox = red_draw.textbbox((0, 0), line, font=big_font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        
        # offset necessary to center the header on the image
        line_offset = int((WIDTH-line_width)/2)
        red_draw.text((line_offset, y_offset), line, font=big_font, fill="black")
        
        # the offset between lines; using the font size as space between each line.
        y_offset += int(0.9*big_font_size)

    # Extra offset in between header and body text
    y_offset += int(0.3 * big_font_size)
    
    # generating the bounding box for the hours
    hours_bbox = black_draw.textbbox((MARGIN, y_offset), hours, font=small_font)
    # print("hours bbox:", hours_bbox)
    # if the big font size ends up not leaving enough room for the hours box, big font must be smaller
    if (hours_bbox[3] > HEIGHT - MARGIN) or (hours_bbox[2] > WIDTH - MARGIN - 250):
        correct_size = False
        
    # increasing the size of the "hours" box to fill empty space
    # this is because if the header is very long/wide, the font will become small and there will be empty space
    # this approach guarantees that small font is at least 0.75 size of big font, but can get bigger to fill extra space
    # small font and big font should probably be called body font and header font!
    if correct_size:
        while not ((hours_bbox[3] > HEIGHT - MARGIN) or (hours_bbox[2] > (WIDTH - MARGIN - 250))): # while the hours bbox is not too big 
            small_font_size += 1
            small_font = small_font = ImageFont.truetype(font=os.path.join(picdir, 'Font.ttc'), size=small_font_size)
            hours_bbox = black_draw.textbbox((MARGIN, y_offset), hours, font=small_font)
    
    black_draw.text((MARGIN, y_offset), hours, font=small_font, fill="black")    
    
    # the spot for the image!
    # black_draw.rectangle((WIDTH-MARGIN-250, HEIGHT-MARGIN-250, WIDTH-MARGIN, HEIGHT-MARGIN))
    bmp_black = Image.open(IMAGE_BMP_DIR+"image_black.bmp")
    bmp_red = None
    if not MONOCOLOR_IMAGE:
        bmp_red = Image.open(IMAGE_BMP_DIR+"image_red.bmp")
        black_image.paste(bmp_black, (WIDTH-MARGIN-250, HEIGHT-MARGIN-250))
        red_image.paste(bmp_red, (WIDTH-MARGIN-250, HEIGHT-MARGIN-250))
    else:
        if MONOCOLOR_BLACK:
            black_image.paste(bmp_black, (WIDTH-MARGIN-250, HEIGHT-MARGIN-250))
        else:
            red_image.paste(bmp_red, (WIDTH-MARGIN-250, HEIGHT-MARGIN-250))
    
    # if the font is too big, then reduce the size. This ensures the largest possible font
    # (for maximum readability) without exceeding the size of the display/margins specified 
    big_font_size -= 1
    
# combine_b_r_images(black_image, red_image) # for testing outside of raspi

from waveshare_epd import epd7in5b_V2_old
#from waveshare_epd import epd7in5_V2

try:
    logging.info("Displaying Image")

    epd = epd7in5b_V2_old.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    epd.display(epd.getbuffer(black_image),epd.getbuffer(red_image))
    
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2_old.epdconfig.module_exit(cleanup=True)
    exit()

exit()
