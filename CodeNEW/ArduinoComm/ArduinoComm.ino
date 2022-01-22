// Libraries and vars
#include <Wire.h> 
#include <dhtnew.h>

//******************************


#include <PID_v1.h> //https://github.com/br3ttb/Arduino-PID-Library

double Setpoint; // Desired value
double Input; // Input pressure value
double Output; // Output fan speed value

//PID paramaters 
double Kp=1.2, Ki=.25, Kd=0.1;

//create PID instance
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, REVERSE);

int readValue = 0; //Raw input signal
int ledValue =0;



//******************************
DHTNEW mySensor(9);

int relay = 2;

int speedPercent = 0; //fan off initially
int freq = 0;
int pressureRaw = 0;
float pressure = 0;
int fluidLevelRaw = 0;
double fluidLevelInch = 0;
float temp = 0;
float humidity = 0;

//Fan Speed: 
//170 - 20%
//255 - 100%
/*********************************************************/
void setup() {
  Serial.begin(9600);
  pinMode(6, OUTPUT);
  pinMode(relay, OUTPUT);

  //*****************
  Setpoint = 159; //0 - 255
  //Turn PID on
  myPID.SetMode(AUTOMATIC);
  //Adjust PID values
  myPID.SetTunings(Kp, Ki, Kd);
  //*****************
  
}

//change fan speed with change in pressure
int speedChange(int pressureRaw){
  if (pressureRaw < 547){ // 547 seems to be equlibirium
    analogWrite(6,0);
    return 0;
  }
  else {
    speedPercent = (pressureRaw-547)/4; //pressure max seems to be 1012, so increase by 4 = 1% increase
    if(speedPercent > 100){ //if speed >100 => totalSpeed > 255 (fan will turn off)
      speedPercent = 100; //so, limit to 100 (can change later using floor function)   
    }
    int totalSpeed = (speedPercent * .85) + 170;
    analogWrite(6, totalSpeed);
    return speedPercent;
  }
}

float levelChange(int rawValue){
  float levelInches = ((float)rawValue / 20) - 25;
  if (levelInches <1){
    return 1.0;
  }
  else if (levelInches>12){
    return 12.0;
  }
  //Serial.println(((float)round(levelInches * 10))/10);
  return ((float)round(levelInches * 10))/10;
}

void loop() {

 
  //freq = analogRead(8); //fan ADC values (?)
  pressureRaw = analogRead(5); 
  speedPercent = speedChange(pressureRaw); //change fan speed based on pressure
  pressure = (float)(analogRead(5)-512)/256; //pressure in kPa 
  fluidLevelRaw = analogRead(10);
  fluidLevelInch = levelChange(analogRead(10));

  if (pressure < 1) {
    digitalWrite(relay, LOW);
  }
  else {
    digitalWrite(relay, HIGH);
  }

  //****************************
  readValue = analogRead(A0);
  //map analog pressureinput signal coming into pin from pin A0 from 0-1024 to 0-255 and set it as Input
  Input = map(pressureRaw, 0, 1024, 0, 255); 
  //Input = readValue; //If you don't need to map to 0-255
  //PID calculation
  myPID.Compute();
  //Write the output as calculated by PID function
  //analogWrite(outputPin, Output); //Set ledPin to PID Output value. This is a PWM pin
  //Send data by serial for plotting
  //Serial.print(millis());
  //Serial.print("\t");
  //Serial.print(map(Input, 0, 255, 0, 100));
  //Serial.print("\t");
  int PIDfanspeed = map(Output, 0, 255, 0, 100);


  //****************************


  
  //temp
  mySensor.read();
  //updateVals(speedPercent, freq, pressureRaw, pressure, analogRead(10), temp);  //user fluidLevelInch for level in inches, then convert updateVals to take float

  temp = (mySensor.getTemperature());
  humidity = (mySensor.getHumidity());
  
  Serial.print(millis());
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(PIDfanspeed);
  Serial.print(",");
  Serial.print(pressureRaw);
  Serial.print(",");
  Serial.print(pressure);
  Serial.print(",");
  Serial.print(fluidLevelRaw);
  Serial.print(",");
  //Serial.print(fluidLevelInch);
  Serial.print(humidity);
  Serial.print("\n");
  
  delay(160);
}
