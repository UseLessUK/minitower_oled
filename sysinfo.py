#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import time
import RPi.GPIO as GPIO
from pathlib import Path
from datetime import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import psutil
import subprocess as sp

# Setup the fan stuff
Fan = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Fan, GPIO.OUT)

p = GPIO.PWM(Fan, 50)
p.start(0)

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

# CPU Usage/Load
def cpu_usage():
    # load average
    av1, av2, av3 = os.getloadavg()
    return "  Ld: %.1f %.1f %.1f " % (av1, av2, av3)

# System Uptime
def uptime_usage():
    # uptime, removal of microseconds solution by: @Berndulas#7599 of the EDCD Discord
    uptime = datetime.now().replace(microsecond=0) - datetime.fromtimestamp(psutil.boot_time())
    return "Up: %s" % (uptime)

# System IP Address
def system_ip():
    # IP
    ip = sp.getoutput("hostname -I").split(' ')[0]
    return "  IP: %s" % (ip)

# Memory Used/Available
def mem_usage():
    usage = psutil.virtual_memory()
    return " Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)

# Space used on Drive
def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "  SD: %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)

# Network traffic
def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

# Get the current CPU Temp and adjust the speed of the Fan based on the temp
def cpu_temp():
    temp = sp.getoutput("vcgencmd measure_temp|egrep -o '[0-9]*\.[0-9]*'")
    if float(temp) < 45.0:
        p.ChangeDutyCycle(20)
        time.sleep(0.1)
        sp.run("moodlight_blue")
    elif float(temp) >= 45.0 and float(temp) < 49.9:
        p.ChangeDutyCycle(50)
        time.sleep(0.1)
        sp.run("moodlight_green")
    elif float(temp) >= 50.0 and float(temp) < 59.9:
        p.ChangeDutyCycle(75)
        time.sleep(0.1)
        sp.run("moodlight_orange")
    elif float(temp) >= 60.0:
        p.ChangeDutyCycle(100)
        time.sleep(0.1)
        sp.run("moodlight_red")
    return " CPU: %s°C" % (temp)

# Output the information to the OLED
def stats(device):
    # use custom font
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    font2 = ImageFont.truetype(font_path, 11)

    # Update the OLED with the required information
    with canvas(device) as draw:
        # CPU usage/load
#        draw.text((0, 1), cpu_usage(), font=font2, fill="white")
        # System IP Address
        draw.text((0,1), system_ip(), font=font2, fill="white")
        if device.height >= 32:
            # Memory used / available
#            draw.text((0, 12), mem_usage(), font=font2, fill="white")
            # CPU usage/load
#            draw.text((0, 12), cpu_usage(), font=font2, fill="white")
            # CPU Temperature
            draw.text((0, 12), cpu_temp(), font=font2, fill="white")
        if device.height >= 64:
            # Space on SSD M.2 Drive, don't forget to change mount point :D
            draw.text((0, 24), disk_usage('/home/pi/m2ssd/'), font=font2, fill="white")
            try:
                # Network card data sent/received
                # If you want the wifi interface then change 'eth0' to 'wlan0' in the following line
                draw.text((0, 36), network('eth0'), font=font2, fill="white")

            except KeyError:
                # no wifi enabled/available
                pass

            # System Uptime
            draw.text((0, 48), uptime_usage(), font=font2, fill="white")

# Grab the OLED Device
device = get_device()

# Do the continuous loop
while True:
    try:
        stats(device)
        time.sleep(5)
    except KeyboardInterrupt:
        pass

# Do some housekeeping
p.ChangeDutyCycle(100)
p.stop()
GPIO.cleanup()
