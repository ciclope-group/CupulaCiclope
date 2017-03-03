#/bin/env python3
# coding:utf-8

import dome_communication as dome
import json
import argparse
import sys

d = dome.Dome()


def help_(a):
        print("""Comandos:
        g N\tGoto N degrees
        s\tShow dome status
        h\tThis help
""")

        
def status(a):
        status = d.get_status()
        print(json.dumps(status))


        
parser = argparse.ArgumentParser(description="Dome test console")
parser.add_argument('-c','--calibrate',action="store_true",help="Perform calibration routine before starting the console")

args = parser.parse_args()
if args.calibrate:
        d.go_home()
        input("Press Enter when the dome is @ home")
        d.calibration_routine()



print("""Consola de pruebas para la cúpula
=================================================""")

#while True:
#        print(d.get_status())

help_(0)
prompt = ">>> "

commands = {
        "s":status,
        "g":d.goto,
        'h':help_}
while True:        
        command = input(prompt)
        order = command.split(" ")
        command = order[0]
        if len(order) >=2:
                arg = int(order[1])
                print("arg: {}".format(arg))
        else:
                arg = 0
        try:
                commands[command](arg)
        except KeyError:
                help(0)
