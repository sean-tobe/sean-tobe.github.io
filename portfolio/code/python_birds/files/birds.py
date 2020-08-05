import os
import sys
import math
import random
import pygame
from pygame.locals import *
import time
from time import sleep
#from mpi4py import MPI

#global vars
FLOCK_MAX = 10

class Bird(pygame.sprite.Sprite):
	height = 0.0
	biomass = 0.0
	diet = ''
	speed = 0
	clock = 0
	isLeft = False
	isAlive = True
	
	def __init__(self, height, biomass, diet):
		pygame.sprite.Sprite.__init__(self)
		self.height = remap(float(height), 0, 3.285, 1, 5.0)
		self.height = limit(self.height, 1, 3)
		self.speed = remap(int(float(biomass)), 0, 50, 1, 10)
		self.speed = limit(self.speed, 1, 10)
		self.biomass = biomass
		self.diet = diet
		# Spawn Rect position
		self.rect = red_left.get_rect()
		if self.diet == 'nectarivore':	# Nectar
			self.rect.x = 0 - self.rect.width
			self.isLeft = False
		elif self.diet == 'frugivore':	# Fruit
			self.rect.x = 1920*5 + self.rect.width
			self.isLeft = True
		else: 							# Insects
			self.rect.x = 0 - self.rect.width
			self.isLeft = False
		self.rect.y = random.randint(2400, 3400)

	def draw(self, screen, off_x, off_y):
		screen.blit(self.image, (self.rect.left - off_x, self.rect.top - off_y))

	def jump(self):
		if self.clock > 30:
			self.clock = 0
			self.speed = int(float(self.biomass))%10
		if self.clock < 15:
			self.speed += self.height
			self.rect.y -= self.speed
		else:
			self.speed -= self.height
			self.rect.y += self.speed
		self.clock += 2
		#if self.gravity % 30 == 0 or self.gravity % 15 == 0: self.gravity = 0
		# if self.gravity % 15 == 0:
		# 	self.gravity = 0
		# elif self.gravity % 15 == 0:
		# 	self.rect.y += self.gravity*int(float(self.height))
		# else:
		# 	self.rect.y -= self.gravity*int(float(self.height))
		# self.gravity += 1
		# print(self.gravity)
		# print(self.rect.y)

	# def left(self):
	# 	self.image = red_left
	# 	self.rect.x -= self.speed

	# def right(self):
	# 	self.image = red_right
	# 	self.rect.x += self.speed

	def update(self, universe_size, flock):
		if self.isAlive == True:
			if self.diet == 'nectarivore':	# Nectar
				if self.rect.left <= 0:
					self.isLeft = False
				if self.rect.right >= universe_size[0]/5*2:
					self.isLeft = True
			elif self.diet == 'frugivore':	# Fruit
				if self.rect.left <= universe_size[0]/5*3:
					self.isLeft = False
				if self.rect.right >= universe_size[0]:
					self.isLeft = True
			else:							# Insects
				if self.rect.left <= universe_size[0]/5*2:
					self.isLeft = False
				if self.rect.right >= universe_size[0]/5*3:
					self.isLeft = True
		elif self.isAlive == False:
			print(self.rect.left)
			if self.rect.left >= universe_size[0]:
				self.kill()
			if self.rect.right <= 0:
				self.kill()

		if self.isLeft == True:
			self.left()
			self.rect.x -= self.speed + 5
		elif self.isLeft == False:
			self.right()
			self.rect.x += self.speed + 5

		hit_list = pygame.sprite.spritecollide(self, flock, False, pygame.sprite.collide_circle_ratio(0.2))
		for bit in hit_list:
			if bit is not self:
				#self.kill()
				if self.isLeft == True:
					self.isLeft = False
				else:
					self.isLeft = True

		self.jump()

		if self.diet == 'nectarivore':	# Nectar
			if self.rect.top <= self.rect.height and self.isLeft == True:
				self.isAlive = False
		elif self.diet == 'frugivore':	# Fruit
			if self.rect.top <= universe_size[1]/3 and self.isLeft == False:
				self.isAlive = False
		else:
			if self.rect.top <= self.rect.height:
				self.isAlive = False


	def get_name(self):
		return self.species

	def get_height(self):
		return self.height

	def get_biomass(self):
		return self.biomass

	def get_diet(self):
		return self.diet

	def get_print(self):
		print('%s | %s | %s' % (self.height, self.biomass, self.diet))

class HAAM(Bird):
	def __init__(self, height, biomass, diet):
		Bird.__init__(self, height, biomass, diet)
		if self.isLeft == True:
			self.image = red_left
		else:
			self.image = red_right

	def left(self):
		self.image = red_left

	def right(self):
		self.image = red_right

class JAWE(Bird):
	def __init__(self, height, biomass, diet):
		Bird.__init__(self, height, biomass, diet)
		if self.isLeft == True:
			self.image = yellow_left
		else:
			self.image = yellow_right

	def left(self):
		self.image = yellow_left

	def right(self):
		self.image = yellow_right

class OMAO(Bird):
	def __init__(self, height, biomass, diet):
		Bird.__init__(self, height, biomass, diet)
		if self.isLeft == True:
			self.image = white_left
		else:
			self.image = white_right

	def left(self):
		self.image = white_left

	def right(self):
		self.image = white_right

class IIWI(Bird):
	def __init__(self, height, biomass, diet):
		Bird.__init__(self, height, biomass, diet)
		if self.isLeft == True:
			self.image = green_left
		else:
			self.image = green_right

	def left(self):
		self.image = green_left

	def right(self):
		self.image = green_right

class APAP(Bird):
	def __init__(self, height, biomass, diet):
		Bird.__init__(self, height, biomass, diet)
		if self.isLeft == True:
			self.image = black_left
		else:
			self.image = black_right

	def left(self):
		self.image = black_left

	def right(self):
		self.image = black_right

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

def read_in(file):
	data = []
	for line in file.readlines():
		bird_data = line.strip().split(',')
		# Check for species
		if bird_data[0] == 'HAAM':
			data.append(HAAM(bird_data[1], bird_data[2], bird_data[3]))
		elif bird_data[0] == 'APAP':
			data.append(APAP(bird_data[1], bird_data[2], bird_data[3]))
		elif bird_data[0] == 'JAWE':
			data.append(JAWE(bird_data[1], bird_data[2], bird_data[3]))
		elif bird_data[0] == 'OMAO':
			data.append(OMAO(bird_data[1], bird_data[2], bird_data[3]))
		elif bird_data[0] == 'IIWI':
			data.append(IIWI(bird_data[1], bird_data[2], bird_data[3]))
	return data

def draw_Image(screen, image, location):
	screen.blit(image, location)

def fill_Background(screen, color):
	screen.fill(color)

def update_Flock(flock, flock_data):
	if len(flock_data) > 0:
		for x in range(FLOCK_MAX - len(flock)):
			flock.add(flock_data.pop(0))
			print('POPP')
	if len(flock) == 0:
		return False
	else:
		return True
	
def text_object(text, font):
    textSurface = font.render(text, True, (255, 255, 127))
    return textSurface, textSurface.get_rect()

def message_Title(screen, text, delta):
    msgText = pygame.font.Font('vhs.ttf',450)
    TextSurf, TextRect = text_object(text, msgText)
    TextRect.left = 0
    TextRect.top = delta
    screen.blit(TextSurf, TextRect)

def message_Text(screen, text, delta):
    msgText = pygame.font.Font('vhs.ttf',100)
    TextSurf, TextRect = text_object(text, msgText)
    TextRect.left = 0
    TextRect.top = delta
    screen.blit(TextSurf, TextRect)

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
pygame.font.init()

# get the screen hight and width
disp_info = pygame.display.Info()
width = disp_info.current_w
height = disp_info.current_h
screen_size = (width,height)
universe_size = (width, height)#(width*5, height*3)

screen = pygame.display.set_mode((screen_size), pygame.NOFRAME)

black_right = pygame.image.load('black.png').convert_alpha()
red_right = pygame.image.load('red.png').convert_alpha()
yellow_right = pygame.image.load('yellow.png').convert_alpha()
green_right = pygame.image.load('green.png').convert_alpha()
white_right = pygame.image.load('white.png').convert_alpha()
white_left = pygame.transform.flip(white_right, True, False)
black_left = pygame.transform.flip(black_right, True, False)
red_left = pygame.transform.flip(red_right, True, False)
yellow_left = pygame.transform.flip(yellow_right, True, False)
green_left = pygame.transform.flip(green_right, True, False)
f1 = pygame.image.load('1.png').convert()
f2 = pygame.image.load('2.png').convert()
f3 = pygame.image.load('3.png').convert()
f4 = pygame.image.load('4.png').convert()
f5 = pygame.image.load('5.png').convert()
f6 = pygame.image.load('6.png').convert()
f7 = pygame.image.load('7.png').convert()
f8 = pygame.image.load('8.png').convert()
f9 = pygame.image.load('9.png').convert()
f10 = pygame.image.load('10.png').convert()
f11 = pygame.image.load('11.png').convert()
f12 = pygame.image.load('12.png').convert()
f13 = pygame.image.load('13.png').convert()
f14 = pygame.image.load('14.png').convert()
f15 = pygame.image.load('15.png').convert()

# read in data and init Birds
file = open("bird_data.csv", "r")
flock_data = read_in(file)
file.close()

flock = pygame.sprite.Group()

curr_time = time.time()

intro = True
while intro:
	comm.Barrier()
	if rank == 0:
		draw_Image(screen, f1, (0, 0))
		message_Title(screen, 'ANGRIER  BIRDS', 5)
		message_Title(screen, '   SEAN TOBE', 450)
		message_Text(screen, '    This is the first line....', 900)
		message_Text(screen, 'This goes on to the second.....', 990)
		message_Text(screen, 'Tour Blog Photos from kateandameer.com expatadventure', 990)
		message_Title(screen, '                         TIDAL  GROWTH', 5)
		pygame.display.update()
	if rank == 1:
		draw_Image(screen, f2, (0,0))
		message_Title(screen, 'ANGRIER  BIRDS', 5)
		pygame.diplay.update()
		
	clock.tick(1)
	py_time = time.time() - curr_time
	if py_time > 5: intro = False

running = False
while running:
	comm.Barrier()
	running = update_Flock(flock, flock_data)

	if rank == 0:
		comm.bcast(flock, root=0)
		draw_Image(screen, f1, (0,0))
		flock.update(universe_size, flock)
		for bird in flock:
			bird.draw(screen, 0, 0)
		pygame.display.update()
	elif rank == 1:
		comm.bcast(flock, root=0)
		draw_Image(screen, f2, (0,0))
		flock.update(universe_size, flock)
		for bird in flock:
			bird.draw(screen, universe_size[0], 0)
		pygame.display.update()
	elif rank == 2:
		comm.bcast(flock, root=0)
		draw_Image(screen, f3, (0,0))
		flock.update(universe_size, flock)
		for bird in flock:
			bird.draw(screen, universe_size[0]*2, 0)
		pygame.display.update()

	clock.tick(30)
	print('#####################LOOP######################')

quit()