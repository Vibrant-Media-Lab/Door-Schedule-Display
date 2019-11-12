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
from waveshare_epd import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from document_interface import * 


logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")
    
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    # epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
    font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), '20', font = font72, fill = 0)
    draw.text((130, 0), 'Vibrant Media Lab', font = font48, fill = 0)
    draw.text((120, 80), 'Student Worker Schedule', font = font24, fill = 0)
    draw.text((610, 0), '20', font = font72, fill = 0)  
    draw.rectangle((10, 100, 630, 360), outline = 2)
    #Name
    draw.rectangle((10, 100, 100, 180), outline = 1)
    #Monday
    draw.rectangle((100, 100, 150, 180), outline = 1)
    #Tuesday
    draw.rectangle((150, 100, 200, 180), outline = 1)
    #Wednesday
    draw.rectangle((200, 100, 250, 180), outline = 1)
    #Thursday
    draw.rectangle((250, 100, 300, 180), outline = 1)
    #Friday
    draw.rectangle((300, 100, 350, 180), outline = 1)

    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    print(get_doc())

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()