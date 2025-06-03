#include <Arduino.h>

int myFunction(int, int);
//int readVal;
int myPin = A5;
int buzzPin = 12;
int delayTime = 2000;
int readNum;
//float V2;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);
  pinMode(myPin, INPUT);
}

void loop() {
  readNum = analogRead(myPin);
  if (readNum>800)
  {
    digitalWrite(buzzPin, HIGH);
    delay(delayTime);
    Serial.println("the value read is:");
    Serial.println(readNum);
    digitalWrite(buzzPin, LOW);
  }
  else
  {
    Serial.println("the value read is:");
    Serial.println(readNum);

  }
  delay(1000);
  
}