from PIL import Image
from PIL import ImageColor
import serial
import sys

#current data format sends 2 bytes per pixel
#1152 pixels for 2304 bytes of data sent
#default baud_rate is 9600
#color components are converted from 8bit to 4bit
#so use wide range in color values

#defaults
img_name = 'image.bmp'
ser_port = '/dev/ttyUSB0'

#parse command line
if (len(sys.argv) > 1):
	if (sys.argv[1] == 'help'):
		print "image file name then serial port" # Option "help"
		exit()
	elif (len(sys.argv) == 3):
		img_name = sys.argv[1]
		ser_port = sys.argv[2]
	else:
		print "Error: bad args"
		exit()

#tests before sending
try:
    img = Image.open(img_name)
except:
    print "Error: Image fine not found"
    exit()

try:
    ser = serial.Serial(ser_port)
except:
    print "Error: Serial port not found"
    exit()

if (img.height != 24 or img.width != 48):
	print "Error: Wrong image size"
	exit()

#wait for start character before sending
print "waiting"
while ser.read() <> 'g':
    pass
    
print "start"
for x in range(48):
    for y in range(24):
        r, g, b = img.getpixel((x,y))
        
        #RGBA uses 8b per, G35 only uses 4b
        temp_MSB = int(b / 16) #the upper 4 bits are not used
        temp_LSB = int(g / 16) * 16 + int(r / 16)
        
        ser.write(chr(temp_MSB))
        ser.write(chr(temp_LSB))
print "done"
        
#there is a "done" byte sent by the sign, ignoring for now
