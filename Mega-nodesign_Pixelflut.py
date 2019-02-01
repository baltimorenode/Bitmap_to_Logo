import serial, sys, time

#local representation of pixels
Frame_Buffer[24][48] = ""
for y in range(24):
	for x in range(48):
		Frame_Buffer[y][x] = "000000"

#Serial port to sign
ser_port = '/dev/ttyUSB0'
baud_rate = 115200

#Network connection
net_port = 1337
throttle = .01

def Get_Pixel (row, col):
	""" To cut down on serial traffic use local frame buffer """
	return str(hex(Frame_Buffer[row][col]))

def Get_Size ():
	return 24, 48

def Help ():
	return """:SUPPORTED COMMANDS:
	HELP - returns this helpfull information
	SIZE - returns screen size (24 by 48)
	PX <x> <y> - get color value of pixel X,Y
	PX <x> <y> <rrggbb> - set color value of pixel X,Y
	           (please note r g b max value is 16)
	"""

def Set_Pixel (row, col, color):
	""" send new pixel to sign then update local frame buffer """
	temp_LSB = 
	temp_MSB = 
	ser = serial.Serial(ser_port, baud_rate)
	ser.write(chr(row))
	ser.write(chr(col))
	ser.write(chr(temp_MSB))
	ser.write(chr(temp_LSB))
	Frame_Buffer[row][col] = color
