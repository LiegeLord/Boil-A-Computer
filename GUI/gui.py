# #Raspberry Pi code to control immersion cooling chamber
# #Authors: Haseeb Irfan, Kevin Antony Gomez, Connor McCreary
# #Trivia of the day: Pluto is not a planet, it is a cartoon dog

#import libraries
from math import sin
from tkinter import W
import dearpygui.dearpygui as dpg
import serial, datetime 
import time
import threading

currentMode = 0 # Light Mode = 0
currentState = 0 # Main, Pressure, Temp, Fan, Level - 0,1,2,3,4 respctively
xAxisP = []
yAxisP = []
xAxisT = []
yAxisT = []
xAxisF = []
yAxisF = []
xAxisL = []
yAxisL = []
time = 0

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

    for i in range (12):
        packet.append(0x00) #2- 13

    #fan mode
    packet.append(0x00) #14

    #fan speed
    packet.append(fanspeed) #15

    #pump power
    packet.append(0x00) #16
    packet.append(pumpLevel) #17

    #other Koolance control bits
    controlBits = ["0x06","0xAE","0xAA","0x00","0x01","0x00","0x01","0x00","0x01"] #18-49
    for bits in controlBits:
        if(bits == "0xAA"): #19 - 43
            for i in range (24): 
                packet.append(hex(int(bits,16)))
        else:
            packet.append(hex(int(bits,16)))

    #parity byte
    packet.append(remainder) #50

    #transmit control signal
    serKool.write(packet)
    print("Command Sent")

    serKool.close()


def changeMode():
    global currentMode
    if(currentMode == 0):
        currentMode = 1
    else:
        currentMode = 0
    nextState(0,0,-1)


def nextState(sender,data,user_data):
        print("Next State")
        # all windows must be deleted pre-transition. Parent window id should suffice
        ids = ["pWindow","tWindow","fWindow","lWindow",
              "currPressWindow","otherPressWindow","pGraphWindow","pGraphWindowInner",
              "currTempWindow", "otherTempWindow", "tGraphWindow","tGraphWindowInner",
              "currLvlWindow", "otherLvlWindow", "lGraphWindow","lGraphWindowInner",
              "currFanWindow","otherFanWindow", "fGraphWindow","fGraphWindowInner"]
        if(user_data != -1):
            global currentState
            currentState = user_data

        for x in ids:
            try:
                dpg.delete_item(x)
            except:
                pass

        if currentState==0:
            createMainPage()
        elif currentState==1:
            createPressurePage()
        elif currentState==2:
            createTempPage()
        elif currentState==3:
            createFanPage()
        elif currentState==4:
            createLevelPage()


def mainLightStyle():
    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (244, 244, 244), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (179, 179, 179), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (179, 179, 179), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0), category=dpg.mvThemeCat_Core)
    with dpg.theme() as data_window_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (244, 244, 244), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (244, 244, 244), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (244, 244, 244), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0), category=dpg.mvThemeCat_Core)
    return window_theme,data_window_theme


def mainDarkStyle():
    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (130, 130, 130), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (130, 130, 130), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 255, 255), category=dpg.mvThemeCat_Core)

    with dpg.theme() as data_window_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255,255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (50, 50, 50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (50, 50, 50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (50, 50, 50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 255, 255), category=dpg.mvThemeCat_Core)
    return window_theme,data_window_theme


def lightStyle():
    with dpg.theme() as window_graph1_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (179, 179, 179 ), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (179, 179, 179 ), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0), category=dpg.mvThemeCat_Core)

    with dpg.theme() as window_graph2_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)

    window_theme,data_window_theme = mainLightStyle()
    return window_theme,data_window_theme, window_graph1_theme,window_graph2_theme


def darkStyle():
    with dpg.theme() as window_graph1_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (130, 130, 130), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (130, 130, 130), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0), category=dpg.mvThemeCat_Core)
    with dpg.theme() as window_graph2_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)

    window_theme,data_window_theme = mainDarkStyle()
    return window_theme,data_window_theme, window_graph1_theme,window_graph2_theme


def displayAlert(valType):
    if valType == 1:
        try:
            pressure = int(dpg.get_value("currPressText").split('p')[0])
            if pressure >= 0.8:
                return True
        except:
            pass
    if valType == 2:
        try:
            temp = int(dpg.get_value("currTempText").split('°')[0])
            if temp >= 56:
                return True
        except:
            pass
    if valType == 3:
        try:
            fanSpeed = int(dpg.get_value("currFanText").split('%')[0])
            if fanSpeed >= 90:
                return True
        except:
            pass
    if valType == 4:
        try:
            lvl = int(dpg.get_value("currLvlText").split("''")[0])
            if lvl <= 2:
                return True
        except:
            pass
    return False


def updatePlot(plotTag, xAxisTag, yAxisTag, xAxis, yAxis):
    # print("vals: ", xAxis, " ", yAxis)
    dpg.set_value(plotTag, [xAxis,yAxis])
    dpg.fit_axis_data(xAxisTag)
    dpg.fit_axis_data(yAxisTag)


def createPressurePage():
    print("pressure")
    with dpg.window(label="Pressure", id="pWindow", width=340, height=730,pos=(0,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_1:
        with dpg.window(id="currPressWindow", width=300, height=100,pos=(20,270),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_1:
            dpg.add_text("Current: - psi", tag="currPressText",pos=(35,25))
        with dpg.window(id="otherPressWindow", width=300, height=170,pos=(20,370),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_2:
            dpg.add_text("Max: - psi",tag="otherPressTextMax",pos=(35,25))
            dpg.add_text("Min: - psi",tag="otherPressTextMin",pos=(35,65))
            dpg.add_text("Run Time: - s",tag="timeRunning",pos=(35,105))
        dpg.add_image("pressIcon",height=100,width=100, pos=(120,100))

    with dpg.window(label="Graph", id="pGraphWindow", width=684, height=730,pos=(340,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_2:
        with dpg.window(id="pGraphWindowInner", width=684, height=560,pos=(340,120),no_collapse=True, no_close=True,no_move=True, no_resize=True, no_title_bar=True) as t1_3:
            with dpg.plot(label="Pressure vs Time",  width=680, height=500, pos=(7,20)):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag = "xAxisPressure")
                dpg.add_plot_axis(dpg.mvYAxis, label="Pressure (psi)", tag="yAxisPressure")
                dpg.add_line_series(xAxisP, yAxisP, parent="yAxisPressure", tag="pressurePlot")

    if(currentMode == 0): # Light Mode
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = lightStyle()
    else:
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = darkStyle()
    
    dpg.bind_item_font("pWindow","title_font")
    dpg.bind_item_font("pGraphWindow","title_font")
    dpg.bind_item_font("currPressText","data_font")
    dpg.bind_item_font("otherPressTextMax","data_font_other")
    dpg.bind_item_font("otherPressTextMin","data_font_other")
    dpg.bind_item_font("timeRunning","data_font_other")

    dpg.bind_item_theme(t1_1, window_theme)
    dpg.bind_item_theme(t1_2, window_graph1_theme)
    dpg.bind_item_theme(t1_3, window_graph2_theme)
    dpg.bind_item_theme(t2_1, data_window_theme)
    dpg.bind_item_theme(t2_2, data_window_theme)


def createTempPage():
    print("temp")
    with dpg.window(label="Temperature", id="tWindow", width=340, height=730,pos=(0,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_1:
        with dpg.window(id="currTempWindow", width=300, height=100,pos=(20,270),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_1:
            dpg.add_text("Current: - psi", tag="currTempText",pos=(35,25))
        with dpg.window(id="otherTempWindow", width=300, height=170,pos=(20,370),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_2:
            dpg.add_text("Max: - °C",tag="otherTempTextMax",pos=(35,25))
            dpg.add_text("Min: - °C",tag="otherTempTextMin",pos=(35,65))
            dpg.add_text("Run Time: - s",tag="timeRunning",pos=(35,105))
        dpg.add_image("tempIcon",height=100,width=100, pos=(120,100))

    with dpg.window(label="Graph", id="tGraphWindow", width=684, height=730,pos=(340,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_2:
        with dpg.window(id="tGraphWindowInner", width=684, height=560,pos=(340,120),no_collapse=True, no_close=True,no_move=True, no_resize=True, no_title_bar=True) as t1_3:
            with dpg.plot(label="Temperature vs Time",  width=680, height=500, pos=(7,20)):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag = "xAxisTemp")
                dpg.add_plot_axis(dpg.mvYAxis, label="Temperature (°C)", tag="yAxisTemp")
                dpg.add_line_series(xAxisT, yAxisT, parent="yAxisTemp", tag="tempPlot")

    if(currentMode == 0): # Light Mode
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = lightStyle()
    else:
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = darkStyle()

    dpg.bind_item_font("tWindow","title_font")
    dpg.bind_item_font("tGraphWindow","title_font")
    dpg.bind_item_font("currTempText","data_font")
    dpg.bind_item_font("otherTempTextMax","data_font_other")
    dpg.bind_item_font("otherTempTextMin","data_font_other")
    dpg.bind_item_font("timeRunning","data_font_other")

    dpg.bind_item_theme(t1_1, window_theme)
    dpg.bind_item_theme(t1_2, window_graph1_theme)
    dpg.bind_item_theme(t1_3, window_graph2_theme)
    dpg.bind_item_theme(t2_1, data_window_theme)
    dpg.bind_item_theme(t2_2, data_window_theme)


def createFanPage():
    print("fan")
    with dpg.window(label="Fan Speed", id="fWindow", width=340, height=730,pos=(0,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_1:
        with dpg.window(id="currFanWindow", width=300, height=100,pos=(20,270),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_1:
            dpg.add_text("Current: - %", tag="currFanText",pos=(35,25))

        if(currentMode == 0): # Light Mode
            dpg.add_image("fanIconLightMode",height=100,width=100, pos=(120,100))
        else:
            dpg.add_image("fanIconDarkMode",height=100,width=100, pos=(120,100))

    with dpg.window(label="Graph", id="fGraphWindow", width=684, height=730,pos=(340,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_2:
        with dpg.window(id="fGraphWindowInner", width=684, height=560,pos=(340,120),no_collapse=True, no_close=True,no_move=True, no_resize=True, no_title_bar=True) as t1_3:
            with dpg.plot(label="Fan Speed vs Time",  width=680, height=500, pos=(7,20)):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag = "xAxisFan")
                dpg.add_plot_axis(dpg.mvYAxis, label="Speed (%)", tag="yAxisFan")
                dpg.add_line_series(xAxisP, yAxisP, parent="yAxisFan", tag="fanPlot")

    if(currentMode == 0): # Light Mode
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = lightStyle()
    else:
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = darkStyle()
    
    dpg.bind_item_font("fWindow","title_font")
    dpg.bind_item_font("fGraphWindow","title_font")
    dpg.bind_item_font("currFanText","data_font")

    dpg.bind_item_theme(t1_1, window_theme)
    dpg.bind_item_theme(t1_2, window_graph1_theme)
    dpg.bind_item_theme(t1_3, window_graph2_theme)
    dpg.bind_item_theme(t2_1, data_window_theme)


def createLevelPage():
    print("lvl")
    with dpg.window(label="Fluid Level", id="lWindow", width=340, height=730,pos=(0,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_1:
        with dpg.window(id="currLvlWindow", width=300, height=100,pos=(20,270),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_1:
            dpg.add_text("Current: - ''", tag="currLvlText",pos=(35,25))

        dpg.add_image("lvlIcon",height=100,width=100, pos=(120,100))

    with dpg.window(label="Graph", id="lGraphWindow", width=684, height=730,pos=(340,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_2:
        with dpg.window(id="lGraphWindowInner", width=684, height=560,pos=(340,120),no_collapse=True, no_close=True,no_move=True, no_resize=True, no_title_bar=True) as t1_3:
            with dpg.plot(label="Fluid Level vs Time",  width=680, height=500, pos=(7,20)):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag = "xAxisLvl")
                dpg.add_plot_axis(dpg.mvYAxis, label="Fluid Level ('')", tag="yAxisLvl")
                dpg.add_line_series(xAxisP, yAxisP, parent="yAxisLvl", tag="lvlPlot")

    if(currentMode == 0): # Light Mode
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = lightStyle()
    else:
        window_theme,data_window_theme,window_graph1_theme,window_graph2_theme = darkStyle()
    
    dpg.bind_item_font("lWindow","title_font")
    dpg.bind_item_font("lGraphWindow","title_font")
    dpg.bind_item_font("currLvlText","data_font")

    dpg.bind_item_theme(t1_1, window_theme)
    dpg.bind_item_theme(t1_2, window_graph1_theme)
    dpg.bind_item_theme(t1_3, window_graph2_theme)
    dpg.bind_item_theme(t2_1, data_window_theme)


def createMenuBar():
    print("menu")
    def show_style(sender):
        dpg.show_style_editor()
            
    with dpg.viewport_menu_bar():
        t0_1 = dpg.add_menu_item(label="Home", callback=nextState, user_data=0, tag="homeBtn")
        t0_2 = dpg.add_menu_item(label="Pressure", callback=nextState, user_data=1, tag="presBtn")
        t0_3 = dpg.add_menu_item(label="Temperature", callback=nextState, user_data=2, tag="tempBtn") 
        t0_4 = dpg.add_menu_item(label="Fan Speed", callback=nextState, user_data=3, tag="fanBtn") 
        t0_5 = dpg.add_menu_item(label="Fluid Level", callback=nextState, user_data=4, tag="lvlBtn") 
        with dpg.menu(label="Settings", tag="settingsBtn") as t0_6:
            dpg.add_menu_item(label="Style Editor", callback=show_style, tag="styleBtn")
            dpg.add_menu_item(label="Change Appearance", callback=changeMode, tag="switchModeBtn")

    with dpg.theme() as menu_bar_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (0, 154, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 20, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, category=dpg.mvThemeCat_Core)

    dpg.bind_item_font("homeBtn","menu_font")
    dpg.bind_item_font("presBtn","menu_font")
    dpg.bind_item_font("tempBtn","menu_font")
    dpg.bind_item_font("fanBtn","menu_font")
    dpg.bind_item_font("lvlBtn","menu_font")
    dpg.bind_item_font("settingsBtn","menu_font")
    dpg.bind_item_font("styleBtn","menu_font")
    dpg.bind_item_font("switchModeBtn","menu_font")

    dpg.bind_item_theme(t0_1, menu_bar_theme)
    dpg.bind_item_theme(t0_2, menu_bar_theme)
    dpg.bind_item_theme(t0_3, menu_bar_theme)
    dpg.bind_item_theme(t0_4, menu_bar_theme)
    dpg.bind_item_theme(t0_5, menu_bar_theme)
    dpg.bind_item_theme(t0_6, menu_bar_theme)


def createMainPage():
    print("main")
    with dpg.window(label="Pressure", id="pWindow", width=512, height=360,pos=(0,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_1:
        with dpg.window(id="currPressWindow", width=200, height=100,pos=(160,160),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_1:
            dpg.add_text("   - psi", tag="currPressText", pos=(50,25))
        if displayAlert(1):
            dpg.add_image("alertOnIcon", height=50, width=50, pos=(400,160))

    with dpg.window(label="Temperature", id="tWindow",  width=512, height=360,pos=(512,20),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_2:
        with dpg.window(id="currTempWindow", width=200, height=100,pos=(668,160),no_collapse=True, no_close=True,no_move=True, no_resize=True)as t2_2:
            dpg.add_text(" - °C", tag="currTempText", pos=(70,25))
        if displayAlert(2):
            dpg.add_image("alertOnIcon", height=50, width=50, pos=(400,160))

    with dpg.window(label="Fan Speed", id="fWindow", width=512, height=360,pos=(0,379),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_3:
        with dpg.window(id="currFanWindow",width=200, height=100,pos=(160,530),no_collapse=True, no_close=True,no_move=True,  no_resize=True)as t2_3:
            dpg.add_text("  - %", tag="currFanText", pos=(65,25))
        if displayAlert(3):
            dpg.add_image("alertOnIcon", height=50, width=50, pos=(400,170))

    with dpg.window(label="Fluid Level", id="lWindow", width=512, height=360,pos=(512,379),no_collapse=True, no_close=True,no_move=True,no_bring_to_front_on_focus=True, no_resize=True) as t1_4:
        with dpg.window(id="currLvlWindow",width=200, height=100,pos=(668,530),no_collapse=True, no_close=True,no_move=True, no_resize=True) as t2_4:
            dpg.add_text("   - ''", tag="currLvlText", pos=(65,25))
        if displayAlert(4):
            dpg.add_image("alertOnIcon", height=50, width=50, pos=(400,170))
        
    if(currentMode == 0): # Light Mode
        window_theme,data_window_theme = mainLightStyle()
    else:
        window_theme,data_window_theme = mainDarkStyle()

    dpg.bind_item_font("pWindow","title_font")
    dpg.bind_item_font("tWindow","title_font")
    dpg.bind_item_font("fWindow","title_font")
    dpg.bind_item_font("lWindow","title_font")

    dpg.bind_item_font("currPressText","data_font")
    dpg.bind_item_font("currTempText","data_font")
    dpg.bind_item_font("currFanText","data_font")
    dpg.bind_item_font("currLvlText","data_font")

    dpg.bind_item_theme(t1_1, window_theme)
    dpg.bind_item_theme(t1_2, window_theme)
    dpg.bind_item_theme(t1_3, window_theme)
    dpg.bind_item_theme(t1_4, window_theme)

    dpg.bind_item_theme(t2_1, data_window_theme)
    dpg.bind_item_theme(t2_2, data_window_theme)
    dpg.bind_item_theme(t2_3, data_window_theme)
    dpg.bind_item_theme(t2_4, data_window_theme)


def getReady():
    # format date and append to .csv name
    dt = datetime.datetime.now()
    dt_str = dt.strftime(" %d-%m-%y %H:%M:%S")
    write_to_file_path = "ArduinoSnifferOutput" + dt_str + ".txt"

    #determine serial port to write to .csv on RPi
    serial_port_2 = '/dev/ttyUSB1';   #this may need to be rewritten depending on your device
    output_file = open(write_to_file_path, "w")

    #open port
    baud_rate = 9600
    return (output_file, serial.Serial(serial_port_2, baud_rate))


def readArduino(name):
    output_file, ser_CSV = getReady()
    while True:
        try:
            line = ser_CSV.readline()
            line = line.decode("utf-8")
            output_file.write(line)
            arr = line.strip().split(",")
            print(arr)

            valuesToSet = {"currPressText":arr[4], "currTempText":arr[1], "currFanText":arr[2],"currLvlText":arr[6]}

            for key in valuesToSet:
                try:
                    dpg.set_value(key, valuesToSet[key])
                except:
                    pass
            
            global time
            time = arr[0]

            try:
                global xAxisP, yAxisP
                if(len(xAxisP) >=25):
                    xAxisP.pop(0)
                    yAxisP.pop(0)
                xAxisP.append(int(time)/1000)
                yAxisP.append(float(valuesToSet["currPressText"]))
                updatePlot("pressurePlot", "xAxisPressure", "yAxisPressure", xAxisP, yAxisP)
            except:
                pass

            try:
                global xAxisT, yAxisT
                if(len(xAxisT) >=25):
                    xAxisT.pop(0)
                    yAxisT.pop(0)
                xAxisT.append(int(time)/1000)
                yAxisT.append(float(valuesToSet("currTempText")))
                updatePlot("tempPlot", "xAxisTemp", "yAxisTemp", xAxisT, yAxisT)
            except:
                pass

            try:
                global xAxisF, yAxisF
                if(len(xAxisF) >=25):
                    xAxisF.pop(0)
                    yAxisF.pop(0)
                xAxisF.append(int(time)/1000)
                yAxisF.append(float(valuesToSet("currFanText")))
                updatePlot("fanPlot", "xAxisFan", "yAxisFan", xAxisF, yAxisF)
            except:
                pass

            try:
                global xAxisL, yAxisL
                if(len(xAxisL) >=25):
                    xAxisL.pop(0)
                    yAxisL.pop(0)
                xAxisL.append(int(time)/1000)
                yAxisL.append(float(valuesToSet("currLvlText")))
                updatePlot("lvlPlot", "xAxisLvl", "yAxisLvl", xAxisL, yAxisL)
            except:
                pass

            try:
                set_koolance(int(arr[2]),10)
            except Exception as inst:
                print(inst)
            
        except:
            pass


def main():
    dpg.create_context() # to access cmds. Must be first
    dpg.create_viewport(title='Microsoft', width=1024, height=740) # outer window in which the gui is displayed
    dpg.set_global_font_scale(1.5)

    with dpg.font_registry():
        dpg.add_font("/Users/kevingomez/Desktop/ENGR 498A-6/code/goodGUI/GUI/assets/fonts/roboto-font/RobotoBold-Xdoj.ttf", 25, tag="data_font")
        dpg.add_font("/Users/kevingomez/Desktop/ENGR 498A-6/code/goodGUI/GUI/assets/fonts/roboto-font/RobotoRegular-3m4L.ttf", 20, tag="data_font_other")
        dpg.add_font("assets/fonts/aquire-font/AquireBold-8Ma60.otf", 14, tag="menu_font")
        dpg.add_font("/Users/kevingomez/Desktop/ENGR 498A-6/code/goodGUI/GUI/assets/fonts/roboto-font/RobotoBoldCondensed-gmVP.ttf", 25, tag="title_font")

    width1, height1, channels1, data1 = dpg.load_image("assets/guiPics/pressure_icon1.png")
    width2, height2, channels2, data2 = dpg.load_image("assets/guiPics/temp_icon1.png")
    width3, height3, channels3, data3 = dpg.load_image("assets/guiPics/fan_icon1.png")
    width4, height4, channels4, data4 = dpg.load_image("assets/guiPics/level_icon1.png")
    width5, height5, channels5, data5 = dpg.load_image("assets/guiPics/alertOn1.png")
    width6, height6, channels6, data6 = dpg.load_image("/Users/kevingomez/Desktop/ENGR 498A-6/code/goodGUI/GUI/assets/guiPics/fan_icon2.png")


    with dpg.texture_registry():
        dpg.add_static_texture(width1, height1, data1, tag="pressIcon")
        dpg.add_static_texture(width2, height2, data2, tag="tempIcon")
        dpg.add_static_texture(width3, height3, data3, tag="fanIconLightMode")
        dpg.add_static_texture(width4, height4, data4, tag="lvlIcon")
        dpg.add_static_texture(width5, height5, data5, tag="alertOnIcon")
        dpg.add_static_texture(width6, height6, data6, tag="fanIconDarkMode")


    createMenuBar()
    createMainPage()

    dpg.setup_dearpygui()
    dpg.show_viewport()

    x =threading.Thread(target = readArduino, args = (1,)) # read and update values in diff thread
    x.start()
    dpg.start_dearpygui() 

    dpg.destroy_context() # must be done to clean up DPG
        

main()





