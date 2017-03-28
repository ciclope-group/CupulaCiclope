
#include "Arduino.h"
enum action {opening=1,closing, stopped, opened,closed};
class shutter{
        action a;
        int error;
        int timeInit;
        int timeFin;
        int oPin, cPin;
        int oSensor, cSensor;
        int maxTime=10000;
        int openTime=5000;

    public:
        shutter(int cS)
        {
            error=0;
            timeInit=0;
            timeFin=0;
            cSensor=cS;
            a=stopped;
            pinMode(5, OUTPUT);
            pinMode(4, OUTPUT);
            pinMode(0, OUTPUT);
            pinMode(2, OUTPUT);
            pinMode(cSensor, INPUT_PULLUP);
        }
        int open(){
            if(digitalRead(cSensor)==0 || a== closing){
                Serial.println("Entro");
                digitalWrite(5, LOW);
                digitalWrite(0, LOW);
                digitalWrite(4, HIGH);
                digitalWrite(2, HIGH);
                timeInit=millis();
                a=opening;
            }
            else if(a!=opening){
                a=stopped;
            }

        }
        int close(){
            if(a==opened || a== opening || a ==stopped){
              digitalWrite(5, HIGH);
              digitalWrite(0, HIGH);
              digitalWrite(4, LOW);
              digitalWrite(2, LOW);
                timeInit=millis();
                a=closing;
            }
            else if(a==closing){
                a=stopped;
            }
        }
        int stop(){
          digitalWrite(5, LOW);
          digitalWrite(0, LOW);
          digitalWrite(4, LOW);
          digitalWrite(2, LOW);
            timeInit=0;
            timeFin=0;
            //a=stopped;
        }
        int getStatus(){

        int status;
          if(digitalRead(cSensor))
             status = opened;
          else { status=closed;}

          return digitalRead(cSensor);
        }
        int checkStatus(){
            switch(a){
                case opening:
                    timeFin=millis();
                    if(timeFin-timeInit>openTime){
                      this->stop();
                      a=opened;
                        return a;
                    }
                    return a;
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
