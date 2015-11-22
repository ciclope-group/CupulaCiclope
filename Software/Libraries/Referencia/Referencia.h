#include <Arduino.h>
#include "/home/pablo//Escritorio/Proyectos/TFG/Software/src/Firmware/pins.h"
extern task t;
void checkString(String s){
	if(s[0]=='M'){
		Serial.println("Entro");
		String s2=String(s[1]);
		if(s[2]!='B')
		s2+=s[2];
		digitalWrite(13,HIGH);
   		delay(s2.toInt()*1000);
   		digitalWrite(13,LOW);
   		
   


	}
	if(s[0]=='R'){
		//int s=String(s[1]);
		int index=0;
		for(int i=0;i<s.length();i++)
		{
			if (s[i]=='#'){
				index=i+1;
				break;
								
			}
		}
		int p;
		digitalWrite(md,HIGH);
		digitalWrite(mi,LOW);
		if(s[1]-'0'==1)p=sensor1;
		if(s[1]-'0'==2)p=sensor2;
		if(s[1]-'0'==3)p=sensor3;

		t.setTask(p,(int)s[index]-'0');
   		
   
	}
	if(s[0]=='L'){
		//int s=String(s[1]);
		int index=0;
		for(int i=0;i<s.length();i++)
		{
			if (s[i]=='#'){
				index=i+1;
				break;
								
			}
		}
		int p;
		digitalWrite(mi,HIGH);
		digitalWrite(md,LOW);
		if(s[1]-'0'==1)p=sensor1;
		if(s[1]-'0'==2)p=sensor2;
		if(s[1]-'0'==3)p=sensor3;

		t.setTask(p,(int)s[index]-'0');
		
   		
   
	}


}