//include libraries
#include <Wire.h> 
#include "TinyDHT.h"
#include <PID_v1.h>

//global value declaration

//PID variables
double Setpoint;                  //desired value
double Input;                     //input pressure value
double Output;                    //output fan speed value
double Kp=1.2, Ki=.25, Kd=0.1;    //PID parameters

//pin values
int relayPin = 3;               //digital
int pressurePin = 5;            //analog
int levelPin = 4;               //analog
int tempPin = 2;                //digital

//reading values
int fanSpeed = 0;           //fan speed
int pressureRaw = 0;        //raw pressure reading (ADC)
float pressurePSI = 0;      //adjusted pressure reading
int fluidLevelRaw = 0;      //raw fluid level
double fluidLevelInch = 0;  //adjusted fluid level
int temp = 0;               //raw temperature reading

//object creation
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, REVERSE);     //PID object instantiation
DHT dht(tempPin, DHT11);                                        //temperature sensor instantiation

//variable to capture realy state
int relayState;

//setup function
void setup() {
  //capture relay state
  int relayState = HIGH;
  
  //start serial communication
  Serial.begin(9600);

  //begin temperature reading
  dht.begin();

  //set pins to output
  pinMode(relayPin, OUTPUT);
  
  //make PID setpoint
  Setpoint = 159; //desired value (range: 0 - 255)
  
  //turn PID on
  myPID.SetMode(AUTOMATIC);
  
  //adjust PID values
  myPID.SetTunings(Kp, Ki, Kd);

}

//function to adjust raw level to inches
float levelChange(int levelRaw){

  //formula for conversion
  float levelInches = ((float)levelRaw / 20) - 25;

  //bounds protection
  if (levelInches < 1){
    return 1.0;
  }
  else if (levelInches > 12){
    return 12.0;
  }
  
  //return final value
  return levelInches;
}

//function to adjust raw pressure to psi
float pressureChange(int pressureRaw){

  //formula for conversion
  float pressurePSI = (float)(pressureRaw - 512) / 512;

  //bounds protection
  if (pressurePSI < -1){
    return -1;
  }
  else if (pressurePSI > 1){
    return 1;
  }
  
  //return final value
  return pressurePSI;
}

//loop function
void loop() {

  //value reading and converting
  pressureRaw = analogRead(pressurePin);             //raw pressure (ADC)
  pressurePSI = pressureChange(pressureRaw);         //adjusted pressure in psi
  fluidLevelRaw = analogRead(levelPin);              //raw level (ADC)
  fluidLevelInch = levelChange(fluidLevelRaw);       //adjusted level in inches

  //electronic pressure valve control based on high pressure
  if (pressurePSI >.5){
    
    //move pin high if not high yet
    if (!relayState){
      relayState = HIGH;
      digitalWrite(relayPin, relayState);
      Serial.println("SWAP");
    }
  }
  
  else{
    
    //move pin low if not low yet
    if (relayState){
      relayState = LOW;
      digitalWrite(relayPin, relayState);
      Serial.println("SWAP");
    }
  }
  
  //map analog pressure input signal coming into pin from pin A0 from 0-1024 to 0-255 and set it as Input
  Input = map(pressureRaw, 0, 1024, 0, 255); 
  
  //PID calculation
  myPID.Compute();

  //scale PID fan speed
  fanSpeed = map(Output, 0, 255, 0, 100);

  //temperature sensor update
  temp = dht.readTemperature(0);

  //temperature bounds protection
  if (temp < 0) {
    temp = 0;
  }
  else if (temp > 100) {
    temp = 100;
  }
 
  //serial communication of measured and converted values to raspberry pi
  Serial.print(millis());
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(fanSpeed);
  Serial.print(",");
  Serial.print(pressureRaw);
  Serial.print(",");
  Serial.print(pressurePSI);
  Serial.print(",");
  Serial.print(fluidLevelRaw);
  Serial.print(",");
  Serial.print(fluidLevelInch);
  Serial.print("\n");

  //delay to transmit
  delay(400);
}
