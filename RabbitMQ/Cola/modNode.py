#!/usr/bin/env python
import sys
outfile = open('config.py', 'r')
targ=sys.argv[1]
arg=sys.argv[2]

outfile.seek(0)
lineas=outfile.readlines()
outfile.close()

lista=arg.split()
for x in lineas:
    if x.find('lista'+targ)!=-1:
        """if x.find(targ)==-1:"""
        lineas[lineas.index(x)]="lista"+targ+' = '+str(lista)

outfile = open('config.py', 'w')
for x in lineas:
    outfile.write(x)
outfile.close()
