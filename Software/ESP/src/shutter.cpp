#include "Arduino.h"
enum action {opening=1,closing, stopped, opened,closed};
class shutter{
        action a;
        int error;
        int timeInit;
        int timeFin;
        int oPin, cPin;
        int oSensor, cSensor;
        int maxTime=5000;

    public:
        shutter(int oS, int cS,int oP,int cP)
        {
            error=0;
            timeInit=0;
            timeFin=0;
            oPin=oP;
            cPin=cP;
            oSensor=oS;
            cSensor=cS;
            a=stopped;
            pinMode(oPin, OUTPUT);
            pinMode(cPin, OUTPUT);
            pinMode(oSensor, INPUT_PULLUP);
            pinMode(cSensor, INPUT_PULLUP);
        }
        int open(){
            if(digitalRead(cSensor)==0 || a== closing){
                Serial.println("Entro");
                digitalWrite(cPin, LOW);
                digitalWrite(oPin, HIGH);
                timeInit=millis();
                a=opening;
            }
            else if(a!=opening){
                a=stopped;
            }

        }
        int close(){
            if(digitalRead(oSensor)==0 || a== opening){
                digitalWrite(oPin, LOW);
                digitalWrite(cPin, HIGH);
                timeInit=millis();
                a=closing;
            }
            else if(a==closing){
                a=stopped;
            }
        }
        int stop(){
            digitalWrite(oPin, LOW);
            digitalWrite(cPin, LOW);
            timeInit=0;
            timeFin=0;
            //a=stopped;
        }
        int checkStatus(){
            switch(a){
                case opening:
                    timeFin=millis();
                    if(timeFin-timeInit>maxTime){
                        this->stop();
                        error=1;
                        return 0;
                    }
                    else {
                        if(digitalRead(oSensor)==LOW){
                            this->stop();
                            a=opened;
                        }
                        return a;
                    }
                    break;
                case closing:
                    timeFin=millis();
                    if(timeFin-timeInit>maxTime){
                        this->stop();
                        error=1;
                        return 0;
                    }
                    else {
                        if(digitalRead(cSensor)==LOW){
                            this->stop();
                            a=closed;
                        }
                        return a;
                    }
                    break;

                case stopped:
                    return a;
                    break;
                default:
                    break;
            }
        }
};
