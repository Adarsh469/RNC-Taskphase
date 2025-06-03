#include <Arduino.h>

int myFunction(int, int);
//int readVal;
//int myPin = A5;
int buzzPin = 13;
int delayTime = 200;
int delayTime2 = 400;
//int readNum;
//float V2;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);
}

void loop() {
  for (int i = 0; i < 100; i++)
  {
    digitalWrite(buzzPin,HIGH);
    delay(delayTime);
    digitalWrite(buzzPin,LOW);
    delay(delayTime);
  }
  for (int i = 0; i < 100; i++)
  {
    digitalWrite(buzzPin,HIGH);
    delay(delayTime2);
    digitalWrite(buzzPin,LOW);
    delay(delayTime2);
  }
  
  
}