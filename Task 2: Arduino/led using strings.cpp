#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);
String msg1 = "enter a string";
String msg2 = "the string entered is:";
String mystring;
int redPin = 12;
int bluePin = 11;
int greenPin = 10;
int delayT = 1000;

void setup() {
    Serial.begin(9600);
    pinMode(redPin,OUTPUT);
    pinMode(bluePin,OUTPUT);
    pinMode(greenPin,OUTPUT);
}

void loop() {
    Serial.println(msg1);
    while (Serial.available()==0)
    {

    }
    mystring = Serial.readString();
    Serial.println(msg2);
    Serial.println(mystring);
    if (mystring == "red")
    {
        digitalWrite(redPin,HIGH);
        delay(delayT);
        digitalWrite(redPin,LOW);
    }
    else if (mystring=="blue")
    {
        digitalWrite(bluePin,HIGH);
        delay(delayT);
        digitalWrite(bluePin,LOW);
    }
    else if (mystring=="green")
    {
        digitalWrite(greenPin,HIGH);
        delay(delayT);
        digitalWrite(greenPin,LOW);
    }
    else{
        Serial.println("invalid input of led");
    }
    
    
}