import serial
import servidorConf as sc
import sys

TICKS_FILE="./.encoder_ticks"
class Dome:
    """Communication with the dome"""

    # Command definitions
    CCW="&L#"
    CW="&R#"
    STOP="&S#"
    EMERGENCY_BREAK="&I#"
    GOHOME="&H#"
    OPEN="&O#"
    CLOSE="&C#"
    CALIBRATE = "&T#"
    STATUS="&G#"
    GOTO="&Z{}#"
    SYNC="&Y{}#"
    SET_HOME="&h{}#"
    SET_ENCODER_FACTOR="&E{}#"
    SET_VMAX_AZIMUT="&J{}#"
    SET_VMIN_AZIMUT="&K{}#"
    SET_ACCEL_AZIMUT="&M{}#"
    SET_RAMP_AZIMUT="&F{}#"
    SET_TICKS_AZIMUT="&z{}#"
    SET_REVERSE_AZIMUT="&K{}#"
    SET_CLOSE_COND="&c{}#"
    short_commands=[
        CCW,
        CW,
        STOP,
        EMERGENCY_BREAK,
        GOHOME,
        OPEN,
        CLOSE,
        CALIBRATE]


    def __init__(self):
        self.encoder_ticks = self.get_ticks_from_file() # Number of ticks the encoder gives in a full turn
        # try :
        #     self.port = serial.Serial(sc.boardPort,9600,timeout=3)
        # except:
        #    print("Error connecting to the board",file=sys.stderr)

    def get_ticks_from_file(self):
        """Returns full turn ticks, fetching the number from persistent storage"""
        f = open(TICKS_FILE)
        line = f.readline()
        f.close()
        if line == "":
            return None
        if line[-1] == "\n":
            line = line[:-1]
        return int(line)


    def store_ticks_to_file(self,number):
        """Stores the argument to persistent storage"""
        f = open(TICKS_FILE,"w")
        f.truncate(0)
        f.write(str(123))
        f.close()


    def send_command(message,process_response):
        """Send a command to the dome controller
        message: string, command which will be sent to the contoller
        process_response: function(string), function to process the response.

        returns the result of executing process_response with the response the controller gives to message if the response is correct, None otherwise"""
        self.port.write(message);
        response = str(self.port.readline())
        if response[0] == "&" and response[-1] == "#":
            return process_response(response)
        return None


    def process_empty_response(response):
        """Processer for those responses which give no extra information"""
        if response == "&#": return 0
        return -1


    def send_short_command(command):
        """Short commands are the ones which have no extra information in the request nor in the response"""
        if command not in short_commands:
            return None
        send_command(command,process_empty_response)

    def send_param_command(command,param):
        """Param commands are the ones which send extra information and recieve empty response"""
        command = encode_long_command(comand,param)
        if command is None: return None
        return send_command(command,process_empty_response)

    def encode_long_command(command,arg):
        """Encodes the argument arg into command so that the controlles understands it and returns the encodes command if everything went ok or None otherwise"""
        if arg < 0:
            print("Cannot send command: negative argument",file=sys.stderr)
            return None

        if arg > 0xFFFFF :
            print("Cannot send command: argument too big",file=sys.stderr)
            return None
        message_bytes = [] # values of the bytes corresponding to the argument
        while arg > 0:
            message_bytes.append((arg%16) + 0x30)
            arg = int(arg / 16)
        while len(message_bytes) < 5: # force 5 character codification
            message_bytes.append(0x30)# append zeroes
        message_bytes.reverse()
        return command.format(bytes(message_bytes).decode())


    def open_shutter(self):
        """Opens the shutter"""
        return send_short_command(OPEN)
    def close_shutter(self):
        """Closes the sutter"""
        return send_short_command(CLOSE)
    def go_home(self):
        """Sends the dome to home position"""
        return send_short_command(GOHOME)
    def clockwise(self):
        """Makes the dome rotate clockwise"""
        return send_short_command(CW)
    def cclockwise(self):
        """Makes the dome rotate counter clockwise"""
        return send_short_command(CCW)
    def stop(self):
        """Makes the dome stop rotating"""
        return send_short_command(CCW)
    def emergency_stop(self):
        """Performs an emergency stop on the dome"""
        return send_short_command(EMERGECY_BREAK)
    def calibrate(self):
        """Performs calibration routine on the dome"""
        return send_short_command(CALIBRATE)

    def azimuth_to_position(self,azimut):
        """Accepts degrees and translates to the position the dome understands"""

        if self.encoder_ticks is None:
            print("Need to calibrate",file=sys.stderr)
            return None
        degrees = azimut % 360
        position = (degrees * self.encoder_ticks)/360
        return position

    def position_to_azimuth(self,position):
        """Accepts dome position and translates to degrees"""
        if self.encoder_ticks is None:
            print("Need to calibrate",file=sys.stderr)
            return None
        degrees = (360*position)/self.encoder_ticks

    def goto(self,azimut):
        """Move the dome to given azimuth (in degrees)"""
        return self.send_param_command(Dome.GOTO,
                                       self.azimuth_to_position(azimut))

    def get_status(self):
        """Gets the status of the dome"""
        def process_status(self,response):
            """Processor for the status of the dome"""
            def decode_value(chars):
                """decodes the value encoded in given chars"""
                value = 0
                for c in chars:
                    value +=(ord(c) & ~8) # most significant bit must be zero
                    value*=256

                return value
            def decode_last_action(char):
                """Decodes the current and last action the dome performed"""
                current = {
                    0:"Running CCW",
                    1:"Stopped",
                    3:"Running CW",
                    4:"Parking",
                    5:"Going home",
                    6:"At home",
                    7:"Calibrating"
                }
                last={
                    0:"None",
                    1:"Run CW by user",
                    2:"Run CCW by user",
                    3:"Stop by user",
                    4:"Goto by user",
                    5:"Calibrate by user",
                    6:"home by user",
                    12:"Motor stalled",
                    13:"Emergency stop"
                }
                current_action_value = ord(char)>>4 & 7 # bits 4,5,6
                last_action_value = ord(char)&0xF# bits 0,1,2,3
                if current_action_value in current:
                    current_action = current[current_action_value]
                else:
                    current_action = "UNKNOWN"
                if last_action_value in last:
                    last_action = last[last_action_value]
                else:
                    last_action = "UNKNOWN"

                return current_action, last_action


            def decode_sensors(chars):
                """Decodes de sensor status"""
                statuses = {
                    10:"Home sensor",
                    11:"Right button",
                    12:"Stop button",
                    13:"Left button"
                }
                #TODO find out codification
                return "None"


            # response: &(G|T)LSxxxyyybbtttll#
            current_action,last_action = decode_last_action(response[2])
            # TODO shutter status decoding (response[3])

            ticks = decode_value(response[4:7]) # positions 4,5,6 (xxx)

            supply = decode_value(response[10:12])# positions 10,11 (bb)
            supply = (supply*15)/1024 # given by vendor

            sensors = decode_sensors(response[15:17])#positions 15,16(ll)

            if response[1] == "T": # Calibration status
                self.store_ticks_to_file(ticks)
                self.encoder_ticks = ticks
                ticks_name = "full_turn"
            else:
                ticks_name = "position"
            return{
                "current_action":current_action,
                "last_action":last_action,
                "supply_voltage":supply,
                "sensors":sensors,
                ticks_name:ticks
            }
        return send_command(Dome.STATUS,process_status)


    def set_home(self,degrees):
        """Sets "home" position of the dome"""
        position = azimuth_to_position(degrees)
        if position is not None:
