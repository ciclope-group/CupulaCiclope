#!/usr/bin/env python
import sys
import config as c
outfile = open('config.py', 'r')
targ=sys.argv[1]
ip=sys.argv[2].split()
arg=ip[2:]
ip=ip[0]

outfile.seek(0)
lineas=outfile.readlines()
outfile.close()
for x in lineas:
    if x.find('listaNodos')!=-1:
        listaNodos2=c.listaNodos[:]
        listaNodos2.append(targ)
        lineas[lineas.index(x)]="listaNodos = "+str(listaNodos2)+"\n"
for x in lineas:
    if x.find('dictIP')!=-1:
        dictIP2=c.dictIP
        var=targ+"IP"
        dictIP2[var]=ip
        lineas[lineas.index(x)]="dictIP = "+str(dictIP2)+"\n"


#lista=arg.split()

lineas.append("lista"+targ+' = '+str(arg))

outfile = open('config.py', 'w')
for x in lineas:
    outfile.write(x)
outfile.close()
