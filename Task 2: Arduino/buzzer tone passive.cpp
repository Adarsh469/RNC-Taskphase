#include <Arduino.h>

int myFunction(int, int);
//int readVal;
//int myPin = A5;
int buzzPin = 13;
int delayTime = 1;
int delayTime2 = 900;
//int readNum;
//float V2;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);
}

void loop() {
  digitalWrite(buzzPin,HIGH);
  delayMicroseconds(delayTime2);
  digitalWrite(buzzPin,LOW);
  delayMicroseconds(delayTime2);
  
}