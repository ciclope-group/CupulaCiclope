String inString = "";    // string to hold input
String str="";
void checkStr(String s){
  if (s=="R"){
	Serial.println("&#");
	 digitalWrite(13,HIGH);}
  if (s=="L"){
	Serial.println("&#");
	digitalWrite(13,HIGH);
	}
  if (s=="I"){
	Serial.println("&#");
	digitalWrite(13,LOW);
	}
 if (s=="G"){ 
        Serial.println("&GLSxxxyyybbtttll#");
        }
}

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  pinMode(13,OUTPUT);

 
 
}



void loop() {
  // Read serial input:
    if (Serial.available() > 0) {
        inString=char(Serial.read());
        
        delay(50);
        if(inString=="&"){
            inString=char(Serial.read());
            delay(50);
            while (inString!="#"){
                str=str+inString;
                inString=char(Serial.read());
                delay(50);
            }
        }
     checkStr(str);   

    }
 inString = "";
 str = "";
   
  /* if(t.checkTask()<0) {
    t.setTask(0,0);
    Serial.println("Fallo Tarea!");
   }*/

}

