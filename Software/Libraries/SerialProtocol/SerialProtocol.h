#include <Arduino.h>
#include </home/pablo/Arduino/libraries/Alarma/Alarm.h>

class SerialProtocol{
	String inString = "";    // string to hold input
	char inChar;
public:
	String read(){
		//Deleting previous values
	    inString = "";
	    inChar=' ';
	    
	      //Reading first byte/////////////
	    inChar =(char) Serial.read();
	    delay(5);
	    if((int)inChar!=10)
	      inString+=inChar; 
	    else return (String)"";
	    //Setting alarm to 1000 ms
	    Alarm a(1000);
	      /////////////////////////////////
	    while(inChar!='B'){
	      //Checking alarm
	        if (!a.checkAlarm()){
	            Serial.println("Fallo Alarma");
	            a.setAlarm(0);
	            return (String)""; 
	        }    
	          
	        inChar =(char)Serial.read();
	        delay(5);
	        if((int)inChar!=10 && (int)inChar!=-1)
	            inString+=inChar; 
	    }
	    //Writing final Byte
	    Serial.read();
	    a.setAlarm(0);
	    Serial.println(inString);
	    return inString;
	    
    }
  

};