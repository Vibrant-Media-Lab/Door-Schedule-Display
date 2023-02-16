#!/usr/bin/python3
import sys
import os
import pathlib

from pathlib import Path

picdir = Path('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic')
libdir = Path('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
else: 
    print('ERROR: Cannot find library...exiting')
    sys.exit()

import logging
import time 
import traceback 

from waveshare_epd import epd7in5
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class DisplayDriver(object): 
    def __init__(self): 
        logging.basicConfig(level=logging.DEBUG)
        self.epd = epd7in5.EPD()
        logging.info("Initializing display...")
        self.epd.init()
        
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        self.font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        self.font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
    
    def display_data(self, data):
        try: 
            self.epd.init()
            Himage = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
            
            draw = ImageDraw.Draw(Himage)
            draw.text((130, 10), 'Vibrant Media Lab', font = self.font48, fill = 0)
            draw.text((250, 65), 'Lab Schedule', font = self.font24, fill = 0)
            draw.rectangle((10, 100, 630, 360), outline = 2)
            
            # grab latest doc 
            lines = data.split('\n')
            for i, line in enumerate(lines): 
                draw.text((15, i*45 + 110), line, font = self.font24, fill = 0)
            
            # get time updated
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y")
            draw.text((15, 335), 'Last updated at {}'.format(dt_string), font = self.font18, fill = 0)

            self.epd.display(self.epd.getbuffer(Himage))

            return True
        except IOError as e:
            print("ERROR: cannot print to display")
            return False

    def cleanup(self):
        epd7in5.epdconfig.module_exit()
