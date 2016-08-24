import os
comando="ps -A | grep py"
tuberia=os.popen(comando)
salida_estandar = tuberia.readlines()
tuberia.close()
for linea in salida_estandar:
        pid= linea.split(" ")[1]
        if "p" in pid:
                pid= linea.split(" ")[0]
        print pid
        os.popen("sudo kill -9 "+ pid)




comando="ps -A | grep mj"
tuberia=os.popen(comando)
salida_estandar = tuberia.readlines()
tuberia.close()
for linea in salida_estandar:
	pid= linea.split(" ")[1]
	if "p" in pid:
		pid= linea.split(" ")[0]
	print pid
	os.popen("sudo kill -9 "+ pid)

