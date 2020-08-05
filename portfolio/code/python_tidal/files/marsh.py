import os
import sys
import math
from math import pi
import random
import pygame
from pygame.locals import *
import time

def read_in(file, paras, temp, hum):
	dates = []
	for line in file.readlines():
		data = line.strip().split(',')
		dates.append((data[0], data[1], data[2], data[3]))
		paras.append(int(float(data[4])))
		temp.append(float(data[5]))
		hum.append(int(data[6]))
	return dates

def draw_Image(screen, image, location):
	screen.blit(image, location)

def fade_image(screen, image, off_x, off_y):
	screen.blit(image, (off_x,off_y))

def blit_marsh(screen, image, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()
        temp.blit(screen, (-x, -y))
        temp.blit(image, (0, 0), None, pygame.BLEND_ADD)
        temp.set_alpha(opacity)        
        screen.blit(temp, location)

def blit_alpha(screen, image, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()
        temp.blit(screen, (-x, -y))
        temp.blit(image, (0, 0))
        temp.set_alpha(opacity)        
        screen.blit(temp, location)

def draw_arc(screen, offset_loc, temp, arc, start_angle, stop_angle, w):
	left = arc[0]
	top = arc[1]
	width = arc[2]
	height = arc[3]
	c01 = 127
	for x in range(0, w):
		c3 = temp + x*5
		c3 = limit(c3, 0, 255)
		for y in range(1, 100):
			pygame.draw.arc(screen, (c01, c01, c3), [left, (top - y - (x*150)), width, height], start_angle, stop_angle, 1)

def remap(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def limit(x, min, max):
	if x <= min:
		x = int(min)
	elif x >= max:
		x = int(max)
	else:
		x = int(x)
	return x

#####################################################################
#comm = MPI.COMM_WORLD
#rank = comm.Get_rank()
#size = comm.Get_size()

# set window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
# get this display
os.environ['DISPLAY'] = ':0.0'

# init clock and display
clock = pygame.time.Clock()
pygame.display.init()

# get the screen hight and width
disp_info = pygame.display.Info()
width = disp_info.current_w
height = disp_info.current_h
screen_size = (width,height)
universe_size = (width*5, height*3)

screen = pygame.display.set_mode((screen_size), pygame.NOFRAME)

b1 = pygame.image.load('b1.png').convert_alpha()
b2 = pygame.image.load('b2.png').convert_alpha()
b3 = pygame.image.load('b3.png').convert_alpha()
b4 = pygame.image.load('b4.png').convert_alpha()
m0 = pygame.image.load('m0.png').convert_alpha()
m1 = pygame.image.load('m1.png').convert_alpha()
m2 = pygame.image.load('m2.png').convert_alpha()
m3 = pygame.image.load('m3.png').convert_alpha()

marsh_temp = [] # 0.0 - 2.55
marsh_hum = []  # 0 - 100
marsh_paras = []

file = open("marsh_data.csv", "r")
marsh_dates = read_in(file, marsh_paras, marsh_temp, marsh_hum)
file.close()

arc = (0,1420,2160,2160)

curr_time = time.time()
end = len(marsh_dates)
counter = 1	# start at [1] for index to [-1]
ticks = 0
fps = 30
while counter <= end:
	comm.Barrier()
	py_time = time.time() - curr_time
		if py_time > 1:
			curr_time = time.time()
			counter += 1
			fps = ticks
			ticks = 0
		else:
			ticks += 1
	#print(counter)
	#print(ticks)
	#print(fps)
	#print((marsh_temp[counter] - marsh_temp[counter-1])/fps)	#interval
	#print(marsh_dates[counter-1])
	#print(marsh_temp[counter-1])
	#print(marsh_hum[counter-1])
	d_temp = (marsh_temp[counter] - marsh_temp[counter-1])/fps
	d_hum = (marsh_hum[counter] - marsh_hum[counter-1])/fps
	d_paras = (marsh_paras[counter] - marsh_paras[counter-1])/fps

	# COLOR
	not_temp = marsh_temp[counter-1] + ticks*d_temp
	temp = remap(not_temp, 0, 30.0, 0, 255)
	temp = limit(temp, 0, 255)

	# GAIN
	not_hum = (marsh_hum[counter-1]) + ticks*d_hum
	hum = remap(not_hum, 0, 100, 0, 10)
	hum = limit(hum, 0, 10)

	# BLIT_ALPHA
	not_paras = (marsh_paras[counter-1]) + ticks*d_paras
	paras = remap(not_paras, 0, 1000, 0, 180)
	paras = limit(paras, 0, 200)

	print('INIT_PARAS: %s | d_paras: %s | PARAS: %s' % (not_paras, d_paras, paras))

	
	if rank == 0:
		draw_image(screen, t1, (0,0))
		draw_arc(screen, (0,0), temp, arc, 0, pi, hum)
		blit_marsh(screen, marsh, (0,0), paras)
		pygame.display.update()
	elif rank == 1:
		draw_image(screen, t2, (0,0))
		draw_arc(screen, (universe_size[0],0), temp, arc, 0, pi, hum)
		blit_marsh(screen, marsh, (0,0), paras)
		pygame.display.update()
	elif rank == 2:
		draw_image(screen, t3, (0,0))
		draw_arc(screen, (0,0), temp, arc, 0, pi, hum)
		blit_marsh(screen, marsh, (0,universe_size[1]), paras)
		pygame.display.update()
	elif rank == 3:
		draw_image(screen, t4, (0,0))
		draw_arc(screen, (universe_size[0],universe_size[1]), temp, arc, 0, pi, hum)
		blit_marsh(screen, marsh, (0,0), paras)
		pygame.display.update()
		
	clock.tick(30)

quit()