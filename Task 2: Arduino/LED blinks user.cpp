#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);
String msg1 = "enter number of blinks";
//String msg2 = "the number entered is:";
int myNumber;
int redPin = 9;
int delayT = 500;

void setup() {
    Serial.begin(9600);
    pinMode(redPin,OUTPUT);

}

void loop() {
    Serial.println(msg1);
    while (Serial.available()==0)
    {

    }
    myNumber = Serial.parseInt();
    while (myNumber>0)
    {
        digitalWrite(redPin,HIGH);
        delay(delayT);
        digitalWrite(redPin,LOW);
        delay(delayT);
        myNumber--;
    }
    Serial.println("enter ");
    while (Serial.available()==0)
    {

    }
    myNumber = Serial.parseInt();
    
    
}