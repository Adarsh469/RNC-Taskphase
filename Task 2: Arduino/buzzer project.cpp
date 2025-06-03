#include <Arduino.h>

int myPin = A5;
int buzzPin = 12;
float potVal;
int freq;

void setup() {
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);
  pinMode(myPin, INPUT);
}

void loop() {
  potVal = analogRead(myPin);
  freq = map(potVal, 0, 1023, 100, 2000);
  
  Serial.print("Potentiometer Value: ");
  Serial.print(potVal);
  Serial.print(" | Frequency: ");
  Serial.println(freq);
  
  tone(buzzPin, freq); 
  
  delay(100); 
}
