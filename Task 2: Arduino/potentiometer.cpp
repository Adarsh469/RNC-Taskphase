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
  V2 = (5./1023.)*readVal;
  if (V2>4){
    Serial.println("your volatge has exceeded 4V i.e: ");
    digitalWrite(warPin, HIGH);
    Serial.println(V2);
  }
  else{
    Serial.println(V2);
  }
  delay(delayTime);
}
