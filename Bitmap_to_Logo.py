#open image file, convert to byte array cols by rows comma separated, then save to file
#the output is not used directly, copy into sketch header file unsigned int array

from PIL import Image
# from PIL import ImageColor

#defaults
image_name = "logo_image.bmp"
data_name = "data.txt"
x_max = 48
y_max = 24

#open image
try:
	source_file = Image.open(image_name, 'r')
except IOError:
	print "Error: Unable to open image file"
	exit()

#image can be smaller, but not larger than 48 col by 24 row
if x_max > source_file.width or y_max > source_file.height:
	print "Error: Image too large"
	exit()

#open data file
try:
	dest_file = open(data_name, 'w') #this should never fail
except IOError:
	print "Error: Unable to open data file"
	exit()

#loop
for y in range(y_max):
	for x in range(x_max):
		#get pixel component colors
		r, g, b = source_file.getpixel((x,y))
		
		#convert pixel value to hex string
		color_val = "0x0" + hex(int(r / 16))[-1] + hex(int(g / 16))[-1] + hex(int(b / 16))[-1] + "U"
		
		#save to data file
		dest_file.write(color_val.upper() + ", ")
	dest_file.write('\n')

#done
dest_file.close()
source_file.close()
print "done"
