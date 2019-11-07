#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
picdir = 'home/pi/e-Paper/RaspberryPi&JetsonNano/python/pic'
libdir = 'home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")
    
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
    font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), '20', font = font72, fill = 0)
    draw.text((160, 0), 'Vibrant Media Lab', font = font48, fill = 0)
    draw.line((255, 15, 360, 15), fill = 0)
    draw.text((120, 20), 'Student Worker Schedule', font = font24, fill = 0)
    draw.text((310, 0), '19', font = font72, fill = 0)  
    draw.rectangle((20, 40, 560, 360), outline = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
