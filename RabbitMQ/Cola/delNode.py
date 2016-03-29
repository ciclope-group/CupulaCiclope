#!/usr/bin/env python
import sys
import config as c
outfile = open('config.py', 'r')
targ=sys.argv[1]

outfile.seek(0)
lineas=outfile.readlines()
outfile.close()
for x in lineas:
    if x.find('listaNodos')!=-1:
        listaNodos2=c.listaNodos[:]
        listaNodos2.remove(targ)
        lineas[lineas.index(x)]="listaNodos = "+str(listaNodos2)+"\n"
for x in lineas:
    if x.find('dictIP')!=-1:
        dictIP2=c.dictIP
        var=targ+"IP"
        del dictIP2[var]
        lineas[lineas.index(x)]="dictIP = "+str(dictIP2)+"\n"
aux="lista"+targ
for x in lineas:
    if x.find(aux)!=-1:

        lineas[lineas.index(x)]=""

outfile = open('config.py', 'w')
for x in lineas:
    outfile.write(x)
outfile.close()
