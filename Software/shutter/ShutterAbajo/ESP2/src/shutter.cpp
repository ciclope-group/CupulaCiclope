
#include "Arduino.h"
enum action {opening=1,closing, stopped, opened,closed};

class shutter{
        action state1;
        action state2;
        int error;
        int timeInit;
        int timeFin;
        int M1,M2,M3,M4;
        int oSensor=14;
        int cSensor=12;
        int SASensor=13;
        int oPin, cPin;
        int maxTime=25000;
        int openTime=15000;
        int aux=0;

    public:
        shutter(int M1,int M2, int M3,int M4,int SASensor, int oSensor,int cSensor)
        {
            error=0;
            timeInit=0;
            timeFin=0;
            this->M1=M1;
            this->M2=M2;
            this->M3=M3;
            this->M4=M4;
            this->SASensor=SASensor;
            this->oSensor=oSensor;
            this->cSensor=cSensor;
            state1=stopped;
            state2=stopped;
            pinMode(M1, OUTPUT);
            pinMode(M2, OUTPUT);
            pinMode(M3, OUTPUT);
            pinMode(M4, OUTPUT);
            pinMode(SASensor, INPUT_PULLUP);
            pinMode(cSensor, INPUT_PULLUP);
            pinMode(oSensor, INPUT_PULLUP);

        }
        int open(){
            if(digitalRead(cSensor)==0 || state1== closing){

                digitalWrite(M1, LOW);
                digitalWrite(M3, LOW);
                digitalWrite(M2, HIGH);
                digitalWrite(M4, HIGH);
                timeInit=millis();
                state1=opening;
            }
            else if(state1!=opening){
                state1=stopped;
            }
            return 0;
        }
        int close(){
            if((state1==opened || state1== opening || state1 ==stopped) && (digitalRead(cSensor)!=0 )){
              digitalWrite(M1, HIGH);
              digitalWrite(M3, HIGH);
              digitalWrite(M2, LOW);
              digitalWrite(M4, LOW);
                timeInit=millis();
                state1=closing;
            }
            else if(state1!=closing){
                state1=stopped;
            }
            return 0;
        }
        int stop(){
          digitalWrite(M1, LOW);
          digitalWrite(M3, LOW);
          digitalWrite(M2, LOW);
          digitalWrite(M4, LOW);
            timeInit=0;
            timeFin=0;
            Serial.println("Paro");
            //a=stopped;
            return 0;
        }
        int getStatus(int *status1,int *status2 ){

             *status1 = state1;
             *status2 = state2;
          return 1;
        }
        int checkStatus(){
            int result1;
            int result2;
            switch(state1){
                case opening:
                    timeFin=millis();
                    if(timeFin-timeInit>openTime){
                      this->stop();
                      state1=opened;
                        result1= state1;
                    }
                    result1= state1;
                    break;
                case closing:
                    timeFin=millis();
                    Serial.println(timeFin-timeInit);
                    if(timeFin-timeInit>maxTime){
                        this->stop();
                        error=1;
                        result1= 0;
                    }
                    else {
                      int a=digitalRead(cSensor);
                      delay(10);
                      int b=digitalRead(cSensor);
                      delay(10);
                      int c=digitalRead(cSensor);

                      if(!a && !b && !c){

                            Serial.println("Bajo");
                            this->stop();
                            state1=closed;
                        }


                        result1= state1;
                    }
                    break;

                case stopped:
                    result1= state1;
                    break;
                default:
                    break;

            }


            int a=digitalRead(SASensor);
            delay(10);
            int b=digitalRead(SASensor);
            delay(10);
            int c=digitalRead(SASensor);

            if(!a && !b && !c){
              state2=opened;
            }
            else{
              state2=closed;
            }

        return 1;

        }
};
