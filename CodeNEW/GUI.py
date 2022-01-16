import pygame, sys, time
import serial
import time

#initialize library
pygame.init()

#functions
def state0(temp, fan, pressure, level):

    #make gray background
    screen.fill(gray_1)

    #draw white rectangles
    pygame.draw.rect(screen,white,(10,10,495,240))
    pygame.draw.rect(screen,white,(517,10,495,240))
    pygame.draw.rect(screen,white,(10,260,495,240))
    pygame.draw.rect(screen,white,(517,260,495,240))

    #bottom dark patch
    pygame.draw.rect(screen,gray_2,(0,510,1024,90))

    #heading background
    pygame.draw.rect(screen,gray_2,(10,10,495,30))
    pygame.draw.rect(screen,gray_2,(517,10,495,30))
    pygame.draw.rect(screen,gray_2,(10,260,495,30))
    pygame.draw.rect(screen,gray_2,(517,260,495,30))

    #white circles for icon background
    tempClick = pygame.draw.circle(screen,white,(112,icon_level),35,0)
    fanClick = pygame.draw.circle(screen,white,(312,icon_level),35,0)
    homeClick = pygame.draw.circle(screen,white,(512,icon_level),35,0)
    pressureClick = pygame.draw.circle(screen,white,(712,icon_level),35,0)
    levelClick = pygame.draw.circle(screen,white,(912,icon_level),35,0)

    #spawn icons
    screen.blit(temp_icon,      (87,icon_level-25))
    screen.blit(fan_icon,       (287,icon_level-25))
    screen.blit(home_icon,      (487,icon_level-25))
    screen.blit(pressure_icon,  (687,icon_level-25))
    screen.blit(level_icon,     (887,icon_level-25))

    #text for headings
    font = pygame.font.SysFont(None, 30)
    img = font.render('Temperature', True, white)
    screen.blit(img, (256 - img.get_width()/2, 15))

    img = font.render('Fan Speed', True, white)
    screen.blit(img, (256 - img.get_width()/2, 265))
    
    img = font.render('Pressure', True, white)
    screen.blit(img, (768 - img.get_width()/2, 15))
    
    img = font.render('Level', True, white)
    screen.blit(img, (768 - img.get_width()/2, 265))

    #write font for data
    font = pygame.font.SysFont(None, 200)

    img = font.render(temp, True, black)
    screen.blit(img, (256 - img.get_width()/2, 80))

    img = font.render(fan, True, black)
    screen.blit(img, (256 - img.get_width()/2, 330))

    img = font.render(pressure, True, black)
    screen.blit(img, (768 - img.get_width()/2, 80))

    img = font.render(level, True, black)
    screen.blit(img, (768 - img.get_width()/2, 330))

    return homeClick, tempClick,fanClick, pressureClick, levelClick

def state1(temp):

    #draw white rectangle
    pygame.draw.rect(screen,white,(10,10,1004,490))

    #draw dark rectangle for heading background
    pygame.draw.rect(screen,gray_2,(10,10,1014,60))

    #write font for heading
    font = pygame.font.SysFont(None, 60)
    img = font.render('Temperature', True, white)
    screen.blit(img, (512 - img.get_width()/2, 20))

    #write font for data
    font = pygame.font.SysFont(None, 450)
    img = font.render(temp, True, black)
    screen.blit(img, (512 - img.get_width()/2, 150))


def state2(fan):

    #draw white rectangle
    pygame.draw.rect(screen,white,(10,10,1004,490))

    #draw dark rectangle for heading background
    pygame.draw.rect(screen,gray_2,(10,10,1014,60))

    #write font for heading
    font = pygame.font.SysFont(None, 60)
    img = font.render('Fan Speed', True, white)
    screen.blit(img, (512 - img.get_width()/2, 20))

    #write font for data
    font = pygame.font.SysFont(None, 450)
    img = font.render(fan, True, black)
    screen.blit(img, (512 - img.get_width()/2, 150))

def state3(pressure):

    #draw white rectangle
    pygame.draw.rect(screen,white,(10,10,1004,490))

    #draw dark rectangle for heading background
    pygame.draw.rect(screen,gray_2,(10,10,1014,60))

    #write font for heading
    font = pygame.font.SysFont(None, 60)
    img = font.render('Pressure', True, white)
    screen.blit(img, (512 - img.get_width()/2, 20))

    #write font for data
    font = pygame.font.SysFont(None, 450)
    img = font.render(pressure, True, black)
    screen.blit(img, (512 - img.get_width()/2, 150))

def state4(level):

    #draw white rectangle
    pygame.draw.rect(screen,white,(10,10,1004,490))

    #draw dark rectangle for heading background
    pygame.draw.rect(screen,gray_2,(10,10,1014,60))

    #write font for heading
    font = pygame.font.SysFont(None, 60)
    img = font.render('Level', True, white)
    screen.blit(img, (512 - img.get_width()/2, 20))

    #write font for data
    font = pygame.font.SysFont(None, 450)
    img = font.render(level, True, black)
    screen.blit(img, (512 - img.get_width()/2, 150))

#common definitions
gray_0 = 128,128,128
gray_1 = 80,80,80
gray_2 = 50,50,50
black = 0,0,0
white = 255, 255, 255
icon_level = 555
state = 0

#set window parameters
size = width, height = 1024, 600
screen = pygame.display.set_mode(size)
screen.fill(gray_1)

#set window details
pygame.display.set_caption("Fluorinert Control System")
MS_icon = pygame.image.load("/home/pi/Desktop/pygameimages/MS_Logo.png")
pygame.display.set_icon(MS_icon)

#load images
fan_icon = pygame.image.load("/home/pi/Desktop/pygameimages/fan_icon.png")
fan_icon = pygame.transform.scale (fan_icon, (50,50))

temp_icon = pygame.image.load("/home/pi/Desktop/pygameimages/temp_icon.png")
temp_icon = pygame.transform.scale (temp_icon, (50,50))

home_icon = pygame.image.load("/home/pi/Desktop/pygameimages/home_icon.png")
home_icon = pygame.transform.scale (home_icon, (50,50))

pressure_icon = pygame.image.load("/home/pi/Desktop/pygameimages/pressure_icon.png")
pressure_icon = pygame.transform.scale (pressure_icon, (50,50))

level_icon = pygame.image.load("/home/pi/Desktop/pygameimages/level_icon.png")
level_icon = pygame.transform.scale (level_icon, (50,50))


#create game loop
running = True
while running:

    temp = 100
    temp = str("tmp")

    fan = 100
    fan = str("fan")

    pressure = 100
    pressure = str("prs")

    level = 100
    level = str("lvl")

    if (state == 0):
        homeClick, tempClick, fanClick, pressureClick, levelClick = state0(temp, fan, pressure, level)
    if state == 1:
        state1(temp)
    if state == 2:
        state2(fan)
    if state == 3:
        state3(pressure)
    if state == 4:
        state4(level)

    #Event sniffer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if homeClick.collidepoint(event.pos):
                state = 0
            if tempClick.collidepoint(event.pos):
                state = 1
            if fanClick.collidepoint(event.pos):
                state = 2
            if pressureClick.collidepoint(event.pos):
                state = 3
            if levelClick.collidepoint(event.pos):
                state = 4

    pygame.display.update()
