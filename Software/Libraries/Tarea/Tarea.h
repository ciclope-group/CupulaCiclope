#include <Arduino.h>
#include </home/pablo/Arduino/libraries/Alarma/Alarm.h>
#include "/home/pablo//Escritorio/Proyectos/TFG/Software/src/Firmware/pins.h"

class task
{
	int pin;
	double tiempo;
	bool enable;
	Alarm alarma;
public:
	task(){
		pin=NULL;
		tiempo=0;
		enable=0;


	}
	void setTask(int p=0, float time=0){
		pin=p;
		alarma.setAlarm(time*1000);
		if (p==0)enable=0;
		else enable=1;

	}
	int checkAlarm(){
		if(!alarma.checkAlarm()){
			digitalWrite(mi,LOW);
			digitalWrite(md,LOW);
			Serial.print("Fallo tarea!");
			return -1;
		}


	}
	int checkTask(){
	
		if(!digitalRead(pin)){ 
			alarma.setAlarm(0);
			digitalWrite(mi,LOW);
			digitalWrite(md,LOW);
			this->setTask(0,0);
			return 1;
		}
		else return -1;

	}
	bool checkEnable(){return this->enable;}




};