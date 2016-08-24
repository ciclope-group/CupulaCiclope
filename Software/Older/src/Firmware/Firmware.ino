#include <Tarea.h>
#include "pins.h"
#include <SerialProtocol.h>
volatile bool flag=0;
volatile long eventTime=0; 
volatile long previousEventTime=0; 
volatile byte portStatus;



#include <Referencia.h>
task t;

String inString = "";    // string to hold input
SerialProtocol sp;
void burpcount()
{
  Serial.println("Hola");
}
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; 
  }
  pinMode(mi,OUTPUT);
  pinMode(md,OUTPUT);
  
  pinMode(sensor1,INPUT_PULLUP);
  pinMode(sensor2,INPUT_PULLUP);
  pinMode(sensor3,INPUT_PULLUP);

  
   PCICR |= (1 << PCIE0);
   PCMSK0 |= (1 << PCINT4);
   PCMSK0 |= (1 << PCINT5);
   PCMSK0 |= (1 << PCINT6);
 
}



void loop() {
  // Read serial input:
  if (Serial.available() > 0) {
    inString=sp.read();
    checkString(inString);
   }
   t.checkAlarm();
  if(flag==1 && (eventTime-previousEventTime)>500 && t.checkEnable()){
      if(t.checkTask()) {
          Serial.println(portStatus,BIN);
          Serial.println("Completado");
          
      }
      flag=0;
  }  
   
  /* if(t.checkTask()<0) {
    t.setTask(0,0);
    Serial.println("Fallo Tarea!");
   }*/

}

 
 ISR (PCINT0_vect){
  flag=1;
  eventTime=millis();
 portStatus=PINB;
  
  
  
  }



