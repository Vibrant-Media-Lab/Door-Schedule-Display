#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os

picdir = '/home/pi/e-Paper/RaspberryPi&JetsonNano/python/pic'
libdir = '/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)
else: 
    print('ERROR: Cannot find library...exiting')
    sys.exit()

import logging
import time 
import traceback 

from waveshare_epd import epd7in5
from PIL import Image,ImageDraw,ImageFont
from document_interface import * 
from datetime import datetime


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        epd = epd7in5.EPD()
        logging.info("Initializing display...")
        epd.init()
        
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
        
        while True:
            epd.init()
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            
            draw = ImageDraw.Draw(Himage)
            draw.text((10, 0), '20', font = font72, fill = 0)
            draw.text((130, 10), 'Vibrant Media Lab', font = font48, fill = 0)
            draw.text((250, 65), 'Lab Schedule', font = font24, fill = 0)
            draw.text((540, 0), '20', font = font72, fill = 0)  
            draw.rectangle((10, 100, 630, 360), outline = 2)
            
            # grab latest doc 
            lines = get_doc().split('\n')[3:8]
            for i, line in enumerate(lines): 
                draw.text((15, i*45 + 110), line, font = font24, fill = 0)
            
            # get time updated
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            draw.text((15, 335), 'Last updated at {}'.format(dt_string), font = font18, fill = 0)

            epd.display(epd.getbuffer(Himage))

            # logging.info("Goto Sleep...")
            # epd.sleep()
            time.sleep(604800)
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5.epdconfig.module_exit()
        exit()
