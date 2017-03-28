
#include "Arduino.h"
enum action {opening=1,closing, stopped, opened,closed};
class shutter{
        action state;
        int error;
        int timeInit;
        int timeFin;
        int oPin, cPin;
        int closeTime;
        int openTime;

    public:
        shutter(int oPin , int cPin, int closeTime, int openTime){
            error=0;
            timeInit=0;
            timeFin=0;
            state=stopped;
            this->oPin=oPin;
            this->cPin=cPin;
            this->closeTime=closeTime*1000;
            this->openTime=openTime*1000;
            pinMode(this->oPin, OUTPUT);
            pinMode(this->cPin, OUTPUT);
        }
        int open(){
            if(state==closed || state== closing || stopped){
                Serial.println("Entro");
                digitalWrite(cPin, LOW);
                digitalWrite(oPin, HIGH);
                timeInit=millis();
                state=opening;
            }
            else if(state!=opening){
                state=stopped;
            }

        }
        int close(){
            if(state==opened || state== opening || state ==stopped){
              digitalWrite(oPin, LOW);
              digitalWrite(cPin, HIGH);
              timeInit=millis();
                state=closing;
            }
            else if(state==closing){
                state=stopped;
            }
        }
        int stop(){
          digitalWrite(cPin, LOW);
          digitalWrite(oPin, LOW);
            timeInit=0;
            timeFin=0;
            state=stopped;
        }
        int OPENED(){
          if(state!=closing){
            digitalWrite(cPin, LOW);
            digitalWrite(oPin, LOW);
              timeInit=0;
              timeFin=0;
              state=opened;
          }
        }
        int getStatus(){

        }
        int checkStatus(){
            switch(state){
                case opening:
                    timeFin=millis();
                    if(timeFin-timeInit>openTime){
                      this->stop();
                      state=opened;
                        return state;
                    }
                    return state;
                    break;
                case closing:
                    timeFin=millis();

                    if(timeFin-timeInit>closeTime){

                        this->stop();
                        error=0;
                        return 0;
                    }
                    else {

                            //this->stop();
                            //state=closed;

                        return state;
                    }
                    break;

                case stopped:
                    return state;
                    break;
                default:
                    break;
            }
        }
};
