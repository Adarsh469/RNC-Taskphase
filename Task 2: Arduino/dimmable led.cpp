#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);
float potVal;
float LEDval;
int myPin = A5;
int LEDpin = 9;
int delayTime = 500;
float V2;


void setup() {
  // put your setup code here, to run once:
  pinMode(myPin, INPUT);
  pinMode(LEDpin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  potVal = analogRead(myPin);
  //V2 = (5./1023.)*readVal;
  LEDval = (255./1023.)*potVal;
  digitalWrite(LEDpin, LEDval);
  delay(delayTime);
}