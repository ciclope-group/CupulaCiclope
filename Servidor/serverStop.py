

import os
comando="ps -A | grep py"
tuberia=os.popen(comando)
salida_estandar = tuberia.readlines()
tuberia.close()
for linea in salida_estandar:
	pid= linea.split(" ")[1]
	print pid
	os.popen("sudo kill -9 "+ pid)

