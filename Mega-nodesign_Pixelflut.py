#!/usr/bin/python
"""
This is a reimplementation of the Pixelflut protocol
Pixel update commands are sent to the Arduino Mega on the sign
All other commands are handled locally in this script
"""

import socket
import threading
import sys, time, serial

class ThreadedServer(object):
    def __init__(self, host, port):
		self.ser_lock = threading.Lock()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.Frame_Buffer = []
        for y in range(24): #fill out local copy of screen contents
            temp = []
            for x in range(48):
			    temp.append('0x000000')
            self.Frame_Buffer.append(temp)

    def listen(self):
        self.sock.listen(5)
        print("Ready for clients")
        while True:
            client, address = self.sock.accept()
            print("CONNECTED:", address)
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def parseCommand(self, conn, cmd):
        print("parsing")
        if cmd == 'QUIT' or cmd == 'EXIT':
            conn.send("Thank you for playing")
            conn.close()
        if cmd == 'HELP':
            conn.send(self.Help())
        if cmd == 'SIZE':
            conn.send("SIZE " + self.Get_Size() + "\r\n")
        if cmd[0:2] == 'PX':
            vals = cmd.split(" ")
            print(vals)
            if len(vals) == 3: #try get
                row = int(vals[1])
                col = int(vals[2])
            if row >=1 and row <=24 and col >=1 and col <=48:
                print("get")
                conn.send("PX " + self.Get_Pixel(row, col)  + "\r\n")
            if len(vals) == 4: #try set
                row = vals[1]
                col = vals[2]
                color = vals[3] #need to add checks on color
        if row >=1 and row <=24 and col >=1 and col <=48:
            self.Set_Pixel(row, col, color)

    def listenToClient(self, client, address):
        while True:
            try:
                data = ''
                while True: #get whole command line
                    c = client.recv(1)
                    if c == '\n' or c == '':
                        break
                    else:
                        data += c
                print(data)
                self.parseCommand(client, data.upper())
            except: #need to find all conditions that end up here
                print("DISCONNECTED", address)
                client.close()
                return False

    def Help (self):
        """ helpfull message for the user """
        return "\t:SUPPORTED COMMANDS:\r\nHELP - returns this helpfull information\r\nSIZE - returns screen size (24 by 48)\r\nPX <x> <y> - get color value of pixel X,Y\r\nPX <x> <y> <rrggbb> - set color value of pixel X,Y\r\n(please note r g b max value is 16)\r\n"

    def Get_Size (self):
        """ the nodesign has a size of 24x48 """
        return "24 48" #size of sign

    def Get_Pixel (self, row, col):
        """ To cut down on serial traffic use local frame buffer """
        return str(self.Frame_Buffer[row][col]) #need to remove "0x" and left pad 0s

    def Set_Pixel (self, row, col, color):
        """ send new pixel to sign then update local frame buffer """
        temp_LSB = int(color[1:1])
        temp_MSB = int(color[3:1]) *16 + int(color[5:])
        if debug:
            print(row, col, color)
        else:
			with ser_lock: #lock around updates
                self.ser.write(chr(row))
                self.ser.write(chr(col))
                self.ser.write(chr(temp_MSB))
                self.ser.write(chr(temp_LSB))
                self.Frame_Buffer[row][col] = color
                self.Create_Send_Image()

    def Pixel_Convert (self, val):
        """ convert '0xRRGGBB' to red, green, blue """
        #separate string into component colors, then convert to int
        red = int("0x" + val[2:4], 16)
        green = int("0x" + val[4:6], 16)
        blue = int("0x" + val[6:8], 16)
        return red, green, blue

    def Create_Send_Image (self):
        """ converts frame buffer to image and uploads that image to webserver """
        im = Image.new('RGB', (480, 240)) # x, y
        r, g, b = 0, 0, 0
        for x in range(48):
            for y in range(24):
                r, g, b = Pixel_Convert(Frame_Buffer[y][x])
                for i in range(10):
                    for j in range(10):
                        im.putpixel((x*10 + i,y*10 + j), (r, g, b))
        im.save('image.bmp') #this is a temp file
        #!!!upload to webserver!!!
        #!!!delete temp file!!!

if __name__ == "__main__":
    port_num = 1337
    ThreadedServer('',port_num).listen()
