import serial, datetime

import pygame, sys, time

#initialize library
pygame.init()


#common definitions
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

tempClick = pygame.draw.circle(screen,white,(112,icon_level),35,0)
fanClick = pygame.draw.circle(screen,white,(312,icon_level),35,0)
homeClick = pygame.draw.circle(screen,white,(512,icon_level),35,0)
pressureClick = pygame.draw.circle(screen,white,(712,icon_level),35,0)
levelClick = pygame.draw.circle(screen,white,(912,icon_level),35,0)




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
    font = pygame.font.SysFont('georgia', 28)
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


def set_koolance(fanspeed, pumpLevel):
     serKool = serial.Serial()
     serKool.port = '/dev/ttyUSB0'
     serKool.baudrate = 9600
     serKool.timeout=0
     serKool.open()
 
     #ser.write(0xCF)
 
     #packet = bytearray()
     #packet.append(0xCF)
     #packet.append(0x01)
     #packet.append(0x08)
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
 
     packet.append(remainder) #50
 
     serKool.write(packet)
     print("Command Sent")
 
     serKool.close()

#start this after starting arduino code (might be fine either way but just to be safe)
state = 0
#will NOT work if serial monitor is open!






def updateGUI(temp, fan, pressure, level, state):

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

    set_koolance(int(fan),10)

    pygame.display.update()
    return state
    


dt = datetime.datetime.now()
dt_str = dt.strftime(" %d-%m-%y %H:%M:%S")

serial_port_2 = '/dev/ttyACM0';   #this may need to be rewritten depending on your device
                        #Use whatever is written at top of serial monitor
baud_rate = 9600;
write_to_file_path = "ArduinoSnifferOutput" + dt_str + ".txt";

output_file = open(write_to_file_path, "w");
ser_CSV = serial.Serial(serial_port_2, baud_rate)
while True:
    line = ser_CSV.readline();
    line = line.decode("utf-8")
    #print(line);
    output_file.write(line);
    
    arr = line.strip().split(",")
    print(arr)
    state = updateGUI(arr[1], arr[2], arr[4], arr[6], state)











