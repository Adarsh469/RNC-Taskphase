#include <Arduino.h>
#include <Servo.h>
// put function declarations here:
int myFunction(int, int);
int servoPin = 9;
int servoPos;
Servo myServo;
void setup() {
    Serial.begin(9600);
    myServo.attach(servoPin);

}

void loop() {
    Serial.println("enter the amount of degrees")
    while (Serial.available()==0)
    {
        /* code */
    }
    servoPos = Serial.parseInt();
    myServo.write(servoPos);
    
    
}