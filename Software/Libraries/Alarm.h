#include <Arduino.h>
class Alarm{
	double inicio;
	double final;
	double tiempo;
public:
	Alarm(double temp=0){
		tiempo=temp;
		inicio=millis();
	
	};
	int checkAlarm(){
		final=millis();
		if (tiempo!=0){
			if ((final-inicio)>tiempo){
				return 0;

			}
			else{ 
				Serial.println(final-inicio);
				return 1;
		
			}
		}



	}
	
};