#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);
String msg1 = "enter a string";
String msg2 = "the string entered is:";
String mystring;

void setup() {
    Serial.begin(9600);
}

void loop() {
    Serial.println(msg1);
    while (Serial.available()==0)
    {

    }
    mystring = Serial.readString();
    Serial.println(msg2);
    Serial.println("myNumber");
    
}