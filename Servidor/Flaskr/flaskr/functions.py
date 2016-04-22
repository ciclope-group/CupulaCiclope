import os
import servidorConf
def send(message,ser):
	if servidorConf.board==1:
		message='&'+message+'#'
		ser.write(message)


def cameraServer():
	os.chdir("/home/trex/TFG/mjpg/mjpg-streamer/")
	print('Video streaming starting on pid',  os.getpid())
	os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0" -o "./output_http.so -w ./www" ')
