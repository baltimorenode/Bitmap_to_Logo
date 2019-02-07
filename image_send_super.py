#current data format sends 2 bytes per pixel, 1152 pixels for 2304 bytes of data sent
#default baud_rate for serial is 9600, takes about 2seconds
#tested working at baud rate 115200, takes less than 1/4second
#color components are down-verted from 8bit to 4bit, so use wide range in color values

from PIL import Image
#from PIL import ImageColor
import serial, sys

#defaults
img_name = 'image'
ser_port = '/dev/ttyUSB0'
frame_count = 1
baud_rate = 115200
extension = ".bmp"
max_row = 24
max_col = 48

#parse command line
if (len(sys.argv) > 1):
	if (sys.argv[1] == 'help'):
        # Option "help"
		print "image file name without extension, then serial port, then image count"
		exit()
	elif (len(sys.argv) == 4):
		#only option pattern has 3 arguments, argv[0] is self
		img_name = sys.argv[1]
		ser_port = sys.argv[2]
		frame_count = int(sys.argv[3])
	else:
		print "Error: bad args"
		exit()

#open serial port
try:
    ser = serial.Serial(ser_port, baud_rate)
except serial.SerialException:
    print "Error: Serial port not found"
    exit()

for i in range(frame_count):
    #open current image file
    try:
        if (frame_count > 1):
            img = Image.open(img_name + str(i + 1) + extension)
        else:
            img = Image.open(img_name + extension)
    except IOError:
        print "Error: Image file not found"
        exit()
    if (img.height != max_row or img.width != max_col):
	    print "Error: Wrong image size"
	    exit()

    #wait for start character before sending
    while ser.read() <> 'g':
    	pass
    
    #send loop for one image
    for x in range(max_col):
    	for y in range(max_row):
			#get pixel component colors
    		r, g, b = img.getpixel((x,y))
			
    		#RGBA uses 8b per, G35 only uses 4b
    		temp_MSB = int(b / 16) #the high 4bits would be brightness
    		temp_LSB = int(g / 16) * 16 + int(r / 16)
			
    		ser.write(chr(temp_MSB))
    		ser.write(chr(temp_LSB))
img.close()
print "done"

#there is a "done" byte sent by the sign, ignoring for now
