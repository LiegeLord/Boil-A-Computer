#Raspberry Pi code to control immersion cooling chamber
#Authors: Haseeb Irfan, Kevin Antony Gomez, Connor McCreary
#Trivia of the day: Pluto is not a planet, it is a cartoon dog

#import libraries
import serial, datetime
import pygame, sys, time

#initialize library
pygame.init()

#common color definitions
gray_0 = 128,128,128
gray_1 = 80,80,80
gray_2 = 50,50,50
black = 0,0,0
white = 255, 255, 255
icon_level = 555

#set window parameters
size = width, height = 1024, 600
screen = pygame.display.set_mode(size)
screen.fill(black)

#set window details
pygame.display.set_caption("Fluorinert Control System")
MS_icon = pygame.image.load("/home/pi/Desktop/pygameimages/MS_Logo.png")
pygame.display.set_icon(MS_icon)

#load images

#fan icon
fan_icon = pygame.image.load("/home/pi/Desktop/pygameimages/fan_icon.png")
fan_icon = pygame.transform.scale (fan_icon, (50,50))

#thermometer icon
temp_icon = pygame.image.load("/home/pi/Desktop/pygameimages/temp_icon.png")
temp_icon = pygame.transform.scale (temp_icon, (50,50))

#house icon
home_icon = pygame.image.load("/home/pi/Desktop/pygameimages/home_icon.png")
home_icon = pygame.transform.scale (home_icon, (50,50))

#pressure gauge icon
pressure_icon = pygame.image.load("/home/pi/Desktop/pygameimages/pressure_icon.png")
pressure_icon = pygame.transform.scale (pressure_icon, (50,50))

#beaker icon
level_icon = pygame.image.load("/home/pi/Desktop/pygameimages/level_icon.png")
level_icon = pygame.transform.scale (level_icon, (50,50))

#objects to detect when icons are clicked
tempClick = pygame.draw.circle(screen,white,(112,icon_level),35,0)
fanClick = pygame.draw.circle(screen,white,(312,icon_level),35,0)
homeClick = pygame.draw.circle(screen,white,(512,icon_level),35,0)
pressureClick = pygame.draw.circle(screen,white,(712,icon_level),35,0)
levelClick = pygame.draw.circle(screen,white,(912,icon_level),35,0)

#initialize state to default screen
state = 0

#functions

#default state to display all values
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
    screen.blit(temp_icon,      (87, icon_level-25))
    screen.blit(fan_icon,       (287,icon_level-25))
    screen.blit(home_icon,      (487,icon_level-25))
    screen.blit(pressure_icon,  (687,icon_level-25))
    screen.blit(level_icon,     (887,icon_level-25))

    #text for headings
    font = pygame.font.SysFont(None, 28)
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

#state to view temperature
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

#state to view fan speed
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

#state to view pressure
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

#state to view fluid level
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

#function to drive Koolance
def set_koolance(fanspeed, pumpLevel):
    
     #open Koolance serial communication
     serKool = serial.Serial()
     serKool.port = '/dev/ttyUSB0'  #may need to adjust depending on USB port Koolance is plugged into
     serKool.baudrate = 9600
     serKool.timeout=0
     serKool.open()
 
     #check fan speed edge cases
     if (fanspeed < 0):
         fanspeed = 0
         
     if (fanspeed > 100):
         fanspeed = 100
     
     if pumpLevel < 0:
         pumpLevel = 0
 
     if pumpLevel > 10:
         pumpLevel = 10
 
     remainder = 0x4A
     remainder = (fanspeed + pumpLevel + remainder) % 100
 
     packet = bytearray()
    
     #unchanged Koolance control bits
     packet.append(0xCF) #0
     packet.append(0x04) #1
 
     packet.append(0x00) #2
     packet.append(0x00) #3
     packet.append(0x00) #4
     packet.append(0x00) #5
     packet.append(0x00) #6
     packet.append(0x00) #7
     packet.append(0x00) #8
     packet.append(0x00) #9
     packet.append(0x00) #10
     packet.append(0x00) #11
     packet.append(0x00) #12
     packet.append(0x00) #13
 
 #fan mode
     packet.append(0x00) #14
    
 #fan speed
     packet.append(fanspeed) #15
 
 #pump power
     packet.append(0x00) #16
     packet.append(pumpLevel) #17
 
 #other Koolance control bits
     packet.append(0x06) #18
     packet.append(0xAE) #19
     packet.append(0xAA) #20
     packet.append(0xAA) #21
     packet.append(0xAA) #22
     packet.append(0xAA) #23
     packet.append(0xAA) #24
     packet.append(0xAA) #25
     packet.append(0xAA) #26
     packet.append(0xAA) #27
     packet.append(0xAA) #28
     packet.append(0xAA) #29
     packet.append(0xAA) #30
     packet.append(0xAA) #31
     packet.append(0xAA) #32
     packet.append(0xAA) #33
     packet.append(0xAA) #34
     packet.append(0xAA) #35
     packet.append(0xAA) #36
     packet.append(0xAA) #37
     packet.append(0xAA) #38
     packet.append(0xAA) #39
     packet.append(0xAA) #40
     packet.append(0xAA) #41
     packet.append(0xAA) #42
     packet.append(0xAA) #43
     packet.append(0x00) #44
     packet.append(0x01) #45
     packet.append(0x00) #46
     packet.append(0x01) #47
     packet.append(0x00) #48
     packet.append(0x01) #49
 
     #parity byte
     packet.append(remainder) #50
 
     #transmit control signal
     serKool.write(packet)
     print("Command Sent")
 
     serKool.close()

#function that updates the GUI's values and process clicks
    
def updateGUI(temp, fan, pressure, level, state):

    #process clicks
    homeClick, tempClick, fanClick, pressureClick, levelClick = state0(temp, fan, pressure, level)
    
    #adjust state
    if state == 1:
        state1(temp)
    if state == 2:
        state2(fan)
    if state == 3:
        state3(pressure)
    if state == 4:
        state4(level)

    #event handler for quitting and clicking icons
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
    
    #adjust koolance speed
    set_koolance(int(fan),10)

    #load new display
    pygame.display.update()
    return state

#format date and append to .csv name
dt = datetime.datetime.now()
dt_str = dt.strftime(" %d-%m-%y %H:%M:%S")
write_to_file_path = "ArduinoSnifferOutput" + dt_str + ".txt";

#determine serial port to write to .csv on RPi
serial_port_2 = '/dev/ttyACM0';   #this may need to be rewritten depending on your device
output_file = open(write_to_file_path, "w");

#open port
baud_rate = 9600;
ser_CSV = serial.Serial(serial_port_2, baud_rate)

while True:
    #copy each transmitted line to .csv
    line = ser_CSV.readline();
    line = line.decode("utf-8")
    output_file.write(line);
    
    #splice line and isolate numbers
    arr = line.strip().split(",")
    print(arr)
    
    #call function to update GUI with proper values
    state = updateGUI(arr[1], arr[2], arr[4], arr[6], state)
