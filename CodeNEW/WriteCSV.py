import serial

#start this after starting arduino code (might be fine either way but just to be safe)

#will NOT work if serial monitor is open!


serial_port = '/dev/ttyACM0';   #this may need to be rewritten depending on your device
                        #Use whatever is written at top of serial monitor
baud_rate = 9600;
write_to_file_path = "ArduinoSnifferOutput.txt";

output_file = open(write_to_file_path, "w");
ser_CSV = serial.Serial(serial_port, baud_rate)
while True:
    line = ser_CSV.readline();
    line = line.decode("utf-8")
    #print(line);
    output_file.write(line);
    
    arr = line.strip().split(",")
    print(arr)
