#include <Arduino.h>
#include <IRremote.h>
int IRpin = 9;
IRrecv IR(IRpin);
decode_results cmd;
void setup()
{
    Serial.begin(9600);
    IR.enableIRIn();
}
void loop()
{
    while (IR.decode(&cmd)==0)
    {
        
    }
    
}