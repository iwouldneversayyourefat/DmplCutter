import cv2
import Image
import numpy as np
import serial
import sys
import math
import os

def getinfo(path):
	img = cv2.imread(path)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # CHAIN_APPROX_SIMPLE less point
	del(contours[0])        # delete the most outer contours
	
	cv2.drawContours(img,contours,-1,(13,52,163),5)

	# find minimum and maximum of x
	left=[]
	right=[]
	top=[]
	foot=[]
	for c in contours:
		pentagram = c
		leftmost = tuple(pentagram[:,0][pentagram[:,:,0].argmin()])
		rightmost = tuple(pentagram[:,0][pentagram[:,:,0].argmax()])
		topmost = tuple(pentagram[:,0][pentagram[:,:,1].argmin()])
		footmost = tuple(pentagram[:,0][pentagram[:,:,1].argmax()])
		
		l=leftmost[0]
		r=rightmost[0]
		t=topmost[0]
		f=footmost[0]
		left.append(l)
		right.append(r)
		top.append(t)
		foot.append(f)
	print left,"\n",right,"\n",top,"\n",foot
	leftm=min(left)
	rightm=max(right)
	topm=min(top)
	footm=max(foot)


	# draw the rectangle contain the words
	(x, y, w, h) = cv2.boundingRect(contours[0])
	cv2.rectangle(img,(leftm, y), (rightm, y + 2), (0, 255, 0), 1)

	print (rightm-leftm)

	cv2.imshow("img", img)
	cv2.waitKey(0)
	return (leftm,rightm,(rightm-leftm),topm,footm)

def vecnzo(ob,size):
	image=cv2.imread(ob)
	info=getinfo(path)
	height,width=image.shape[:2]
	w=info[2]
	rate=float(255)/float(w)
	rate2=13.68*size/9
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	es=cv2.resize(gray,(int(width*rate*rate2),int(height*rate*rate2)),interpolation=cv2.INTER_CUBIC)
	ret, binary = cv2.threshold(es,127,255,cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	del(contours[0])
	file=open("1.txt","w")
	file.write(";:H A L0 ECN U V10")  # init the cutter

	for c in contours:
		file.write(" ")
		a=0
		file.write(" U")
		for d in c:
			for tables in d:
					for item in tables:
						file.write(str(item))
						a+=1
						if(a==2):
							file.write(" D")
						else:
							file.write(",")
		tail=c[0][0]
		file.write(str(tail[0]))
		file.write(",")
		file.write(str(tail[1]))
	a=0
	file.close()
	
	file = open("1.txt","r")
	con = file.read()
	t = serial.Serial('com1',9600)
	n = t.write(con)

path="1.jpg"
size=float(raw_input("size in cm:"))
vecnzo(path,size)

