#include <Arduino.h>

float readVal;
int myPin = A5;
int redPin = 13;
int bluePin = 12;

int delayTime = 500;


void setup() {
  // put your setup code here, to run once:
  pinMode(myPin, INPUT);
  pinMode(redPin,OUTPUT);
  pinMode(bluePin,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  readVal = analogRead(myPin);
  Serial.println("the voltage is:");
  Serial.println(readVal);
  if (readVal<250)
  {
    digitalWrite(bluePin,HIGH);
    digitalWrite(redPin,LOW);
  }
  else{
    digitalWrite(redPin,HIGH);
    digitalWrite(bluePin,LOW);
  }
  


  delay(delayTime);
}