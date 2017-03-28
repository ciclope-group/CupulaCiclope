#include <ESP8266WiFi.h>
#include "shutter.cpp"

const char* ssid     = "TP-LINK_EB1428";
const char* password = "grupociclope";
IPAddress ip(192,168,1,10);  //Node static IP
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);
int M1 = 5, M2=4, M3 = 0, M4=2;
int SASensor=13, oSensor=14, cSensor=  12;  // GPIO13
WiFiServer server(80);
WiFiClient client;
bool wRequest;
shutter s(M1,M2,M3,M4,SASensor,oSensor,cSensor);
int prevSA=closed;
int state=0;
void setup() {
  Serial.begin(9600);
  delay(10);


  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  WiFi.config(ip, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

}

void loop() {
  // Check if a client has connected
  String request;
  String url;
  int value;
  WiFiClient client = server.available();
  if (!client) {
    wRequest=1;
  }
  else {wRequest=0;};
  // Wait until the client sends some dataco
  int timein=millis();
  switch(wRequest){
    case 0:
      Serial.println("new client");

      while(!client.available()){
        delay(1);
        int timeFin=millis();

        if(timeFin-timein>1000){
          client.flush();
          break;

        }
        Serial.println("Me quedo");
      }

      // Read the first line of the request
      request = client.readStringUntil('\r');
      Serial.println(request);

      /*if (request.indexOf("/status") != -1)  {
        if (client.connect("cupula.datsi.fi.upm.es", 5000)){}
        Serial.println("WiFi Client connected ");
        client.print(String("POST ") + url + " HTTP/1.1\r\n" +
                   "Host: " + "cupula.datsi.fi.upm.es:5000" + "\r\n" +
                   "Connection: close\r\n\r\n");
        Serial.print("Sended POST");
    }*/
    Serial.println("Llego");
    if (request.indexOf("/statusUp") != -1)  {

      int st[2];
      s.getStatus(&st[0],&st[1]);
      String s1, s2;
      if (st[0]==opened){ s1="opened" ;}
      if (st[0]==closed){ s1="closed"; }
      else {  s1="undefined";}
      if (st[1]==opened){  s2="opened" ;}
      if (st[1]==closed){  s2="closed"; }
      else { String s2="undefined";  }

      Serial.println(s2);
      client.println(s2);
      client.stop();

  }
  else if (request.indexOf("/statusDown") != -1)  {

    int st[2];
    s.getStatus(&st[0],&st[1]);
    String s1, s2;
    if (st[0]==opened){ s1="opened" ;}
    else if (st[0]==closed){ s1="closed"; }
    else {  s1="undefined";}
    if (st[1]==opened){  s2="opened" ;}
    if (st[1]==closed){
     s2="closed"; }
    else { String s2="undefined";  }

    Serial.println(s1);
    client.println(s1);
    client.stop();


}

      // Match the request


      else if (request.indexOf("/Open") != -1)  {
        //digitalWrite(ledPin, HIGH);
        Serial.println("Abriendo");
        s.open();

      }
      else if (request.indexOf("/Close") != -1)  {
        //digitalWrite(ledPin, LOW);
        s.close();
      }

    // Set ledPin according to the request


      // Return the response
      /*client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: text/html");
      client.println(""); //  do not forget this one
      client.println("<!DOCTYPE HTML>");
      client.println("<html>");*/

      /*client.print("State is now: ");

      switch(state){
        case opening:
            client.print(String("opening"));
            break;
        case closing:
            client.print(String("closing"));
            break;
        case opened:
            client.print(String("opened"));
            break;
        case closed:
            client.print(String("closed"));
            break;
        case stopped:
            client.print(String("stopped"));
            break;
        case 0:
            client.print(String("error"));
            break;
        default:
        break;
      }*/
      /*
      client.println("<br><br>");
      client.println("<a href=\"/Abrir\"\"><button>Abrir </button></a>");
      client.println("<a href=\"/Cerrar\"\"><button>Cerrar </button></a><br />");
      client.println("</html>");
      */
      delay(1);
      Serial.println("Client disonnected");
      Serial.println("");

      break;

  case 1: {
    s.checkStatus();
    state=0;
    int st[2];
    s.getStatus(&st[0],&st[1]);
    //Serial.println(res[1]);

    if (prevSA==closed && st[1]==opened){

      /*client.println("GET /Parar HTTP/1.1");
  client.print("Host: 10.42.0.11");
  client.println("Connection: close");
  client.println();*/
  if (client.connect("192.168.1.11", 80)){
  Serial.println("WiFi Client connected ");
  client.print(String("GET ") + "/Opened" + " HTTP/1.1\r\n" +
             "Host: " + "10.42.0.11:80" + "\r\n" +
             "Connection: close\r\n\r\n");}
      Serial.println("Petición Hecha");
      //client.print(String("GET") + " /Parar" + " HTTP/1.1\r\n" + "Host: 10.42.0.11" + "\r\n\r\n");
      client.flush();
      delay(1000);

      // Read all the lines of the reply from server and print them to Serial

    }
    prevSA=st[1];


    //if(!s.checkStatus())Serial.println("Alarma");
    /*
      if (digitalRead(buttonPin)!=HIGH) Serial.println("Pulsado");
      break;
      */
    }
  default:
        break;
  }
}
