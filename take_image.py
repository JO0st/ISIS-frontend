#! /usr/bin/python

import subprocess
import socket
import re
import os
from take_image import *

def take_picture():
	result = os.popen('sudo raspistill -o /home/isis/ISIS-frontend/image.jpg').read()
	if re.match('failed', result) is None:
		sleep("5")
		os.system("scp  /home/isis/ISIS-frontend/image.jpg isis@192.168.255.54:/home/isis/Afbeeldingen/image.jpg")
	else:
		raise Exception("Camera is not found! (or some other error)")