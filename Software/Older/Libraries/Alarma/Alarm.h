#include <Arduino.h>
#ifndef ALARMA_H
#define ALARMA_H
class Alarm{
	double inicio;
	double final;
	double tiempo;
	bool enable;
public:
	Alarm(double temp=0){
		tiempo=temp;
		inicio=millis();
		enable=1;
		if (temp==0)
			enable=0;
	
	}
	int checkAlarm(){
		final=millis();
		//Serial.println(tiempo);
		if (enable){
			if ((final-inicio)>tiempo)
				return 0;
			else return 1;
		}	
		return 1;



	}
	int setAlarm(double temp){
		inicio=millis();
		tiempo=temp;
		enable=1;
		if(temp==0)
		enable=0;
	}
	
};
#endif