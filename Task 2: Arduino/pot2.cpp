#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);
int readVal;
int myPin = A5;
int warPin = 9;
int delayTime = 500;
float V2;


void setup() {
  // put your setup code here, to run once:
  pinMode(myPin, INPUT);
  pinMode(warPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  readVal = analogRead(myPin);
  Serial.println(readVal);
  delay(delayTime);
  //V2 = (5./1023.)*readVal;
  while (readVal>1000){
    digitalWrite(warPin,HIGH);
    readVal = analogRead(myPin);
    Serial.println("pot. value: ");
    Serial.println(readVal);
    delay(delayTime);
  }
  digitalWrite(warPin,LOW);
  delay(delayTime);
}
