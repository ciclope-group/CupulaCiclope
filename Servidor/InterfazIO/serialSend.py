import serial
import sys
ser = serial.Serial('/dev/ttyACM0', 9600)
message ="".join(sys.argv[1:])
ser.write(message)
ser.close()