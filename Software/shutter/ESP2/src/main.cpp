#include <ESP8266WiFi.h>
#include "shutter.cpp"

const char* ssid     = "TP-LINK_EB1428";
const char* password = "grupociclope";
IPAddress ip(192,168,1,129);  //Node static IP
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);
int M1 = 5, M2=4; // GPIO13
int cSensor=13;
WiFiServer server(80);
WiFiClient client;
bool wRequest;
shutter s(cSensor);
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
  // Wait until the client sends some data
  switch(wRequest){
    case 0:
      Serial.println("new client");
      while(!client.available()){
        delay(1);
      }

      // Read the first line of the request
      request = client.readStringUntil('\r');
      Serial.println(request);
      client.flush();
      url="/status";
      /*if (request.indexOf("/status") != -1)  {
        if (client.connect("cupula.datsi.fi.upm.es", 5000)){}
        Serial.println("WiFi Client connected ");
        client.print(String("POST ") + url + " HTTP/1.1\r\n" +
                   "Host: " + "cupula.datsi.fi.upm.es:5000" + "\r\n" +
                   "Connection: close\r\n\r\n");
        Serial.print("Sended POST");
    }*/
    if (request.indexOf("/status") != -1)  {
      /*switch(state){
        case opening:
            client.print(String("opening"));
            break;
        case closing:
            client.print(String("closing"));
            break;
        case opened:
            if (s.getStatus()==opened)client.print(String("opened"));
            else{client.print(String("opened sin verificar"));}
            break;
        case closed:
            if (s.getStatus()==closed)client.print(String("closed"));
            else{client.print(String("closed sin verificar"));}

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
      client.print(String(digitalRead(cSensor)));
    }
      // Match the request

else{

      if (request.indexOf("/Abrir") != -1)  {
        //digitalWrite(ledPin, HIGH);
        s.open();

      }
      if (request.indexOf("/Cerrar") != -1)  {
        //digitalWrite(ledPin, LOW);
        s.close();
      }

    // Set ledPin according to the request


      // Return the response
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: text/html");
      client.println(""); //  do not forget this one
      client.println("<!DOCTYPE HTML>");
      client.println("<html>");

      client.print("State is now: ");

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
        }

      client.println("<br><br>");
      client.println("<a href=\"/Abrir\"\"><button>Abrir </button></a>");
      client.println("<a href=\"/Cerrar\"\"><button>Cerrar </button></a><br />");
      client.println("</html>");

      delay(1);
      Serial.println("Client disonnected");
      Serial.println("");

      break;
  }
  case 1:
    state=s.checkStatus();
    if(!s.checkStatus())Serial.println("Alarma");
    /*
      if (digitalRead(buttonPin)!=HIGH) Serial.println("Pulsado");
      break;
      */
  default:
        break;
  }
}
