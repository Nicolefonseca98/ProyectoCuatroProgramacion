from socket import *
from _thread import *
import time
import sys
import json
import threading

#Variables globales
aceptaConexiones = True  		#Acepta conexiones de los clientes.
lista_de_clientes = []   		#Lista de clientes que se conectan, guarda el numero del cliente.
lista_respuestas = []  			#Lista de respuestas a evaluar, se guarda el numero del cliente y la respuesta.
diccionario = {}		 		#Diccionario que contiene las preguntas y sus respuestas.
lista_preguntas = []			#Lista con las preguntas a realizar.
lista_conexiones = []			#Guarda la conexion de cada cliente.
lista_hilos_cliente = []		#Guarda el hilo de cada cliente para empezar a recibir respuestas.
ranking = {}					#Guarda las respuestas correctas de cada cliente para mostrar un ranking
								# al final de cada partida.
historial = {}					#Guarda todas las preguntas realizadas y el jugador que contestó correctamente

#Funciones
#Pide host y puerto.
def ini():
    host = input("Host: ")
    port = int(input("Puerto: "))
    return host, port

#Crea un nuevo socket.
def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

#Intenta ligar un socket con los parametros host y port.
def ligarSocket(socket, host, port):
    while True:
        try:
            socket.bind((host, port))
            break
        except error as e:
            print("No se puede conectar.")

#Espera por la conexión de clientes.
def conexiones(socket):
    conn, addr = socket.accept()
    print("\nConexion Establecida.\nEl jugador es: ", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

#Envia un mensaje codificado a la direccion de los clientes.
def enviar(conn, mensaje):
    try:
       	conn.send(mensaje.encode("UTF-8"))
    except:
        print("\nNo se pudo enviar\n")
        print("Nuevo intento en 5 seg\n")
        time.sleep(5)

#Lee el archivo y llena el diccionario con la pregunta y su respuesta
# y una lista solo con las preguntas.
def leerJson():
	global diccionario, lista_preguntas
	print("**Cargar archivo con preguntas**")
	archivo = input("Nombre del archivo: ")
	with open(archivo) as preguntas:
		pregunta = json.load(preguntas)
		for x in pregunta:
			diccionario[x.get('enunciado')] = x.get('respuestas')
			lista_preguntas.append(x.get('enunciado'))

#Mensajes recibidos de los distintos clientes.
#Llama a la funcion cuando recibe mensajes de los clientes.
def recibir(conn):
	global lista_de_clientes
	while True:
		try:
			reply = conn.recv(2048)
			reply = reply.decode("UTF-8")
			for x in lista_de_clientes:
				if reply[0] == str(x):
					print("Jugador ", reply)
					lista_respuestas.append(reply[0]+reply[3:len(reply)])
		except:
		   	print("No se pudo recibir respuesta.")
		   	time.sleep(5)
	

#Verifica si en la lista se encuentra la respuesta correcta de la pregunta 
# que ingresa como parametro.
def verificaRespuesta(pregunta):
	mensaje = False
	global diccionario, lista_respuestas, ranking, lista_conexiones
	for x in diccionario:
		if x == pregunta:
			for i in lista_respuestas:
				respuesta = i[1:len(i)]
				for y in diccionario[x]:
					if respuesta.lower() == y.lower():
						existeJugador, count= revisaRanking(i[0])
						if existeJugador:
							ranking['Respuestas correctas jugador ',i[0]] = count
						else:
							ranking['Respuestas correctas jugador ',i[0]] = 1
						for conexion in lista_conexiones:
							msj = {"mensaje": "informacion", "valor": "Respuesta correcta del jugador " + i[0]}
							msjJson = json.dumps(msj)
							enviar(conexion, msjJson)
						return True, i[0]
						break
					else:
						pass
	return False, 0

#Revisa si en el ranking ya existe un jugador con respuestas correctas para
#actualizar el numero de las mismas.
def revisaRanking(jugador):
	global ranking
	for x in ranking:
		if x[1] == jugador:
			count = ranking[x]
			count = int(count) + 1
			ranking.pop(x)
			return True, count
		else:
			pass
	return False, 0

          
#El servidor asigna un numero a cada cliente y lo envia.
def enviarNumeroJugador(conn, numeroCliente):
    global lista_de_clientes
    msj = {"mensaje": "conexion", "valor": "Bienvenido jugador " + str(numeroCliente)}
    msjJson = json.dumps(msj)
    conn.send(msjJson.encode("UTF-8"))

#Método para enviar una pregunta a la vez a los jugadores.
def enviarPregunta(counter):
	global lista_preguntas
	return lista_preguntas[counter]

#Revisa en el ranking cual es el jugador con más respuestas acertadas
#para determinar un ganador.
def ganador():
	global ranking
	a = 0
	for x in ranking:
		if a < int(ranking[x]):
			a = int(ranking[x])
		else:
			pass
	for y in ranking:
		if a == ranking[y]:
			return str(y[1])

#Muestra el ranking al final de la partida.
def mostrarRanking():
	global ranking
	mensaje = ""
	for x in ranking:
		mensaje += str(x) + str(ranking[x]) + "\n"
	return mensaje

#Muestra el historial al final de la partida.
def mostrarHistorial():
	global historial
	mensaje = ""
	for x in historial:
		mensaje += str(x) +"\n"+ str(historial[x]) + "\n"
	return mensaje

#Método main
def main():
    global lista_conexiones, lista_preguntas, lista_hilos_cliente, aceptaConexiones, ranking, historial
    leerJson()
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(9)  
    counter = 0

    print("\nFase de conexiones.","\nEsperando por los jugadores.")
    cantidadClientes = 1

    #Fase de conexiones
    while aceptaConexiones == True:
    	conn, addr = conexiones(s)
    	enviarNumeroJugador(conn, cantidadClientes)
    	lista_de_clientes.append(str(cantidadClientes))
    	lista_conexiones.append(conn)
    	hilo = threading.Thread(target= recibir, args=(conn,))
    	lista_hilos_cliente.append(hilo)
    	print("\n*Esperando jugadores*")
    	msj = {"mensaje": "informacion", "valor": "Esperando Jugadores"}
    	msjJson = json.dumps(msj)
    	enviar(conn, msjJson)
    	cantidadClientes = cantidadClientes + 1
    	if len(lista_de_clientes) >= 2:
    		pregunta = input("¿Desea comenzar el juego? Ingrese si o no: ")
    		if pregunta == "no":
    			for conexion in lista_conexiones:
    				msj = {"mensaje": "informacion", "valor": "Esperando Jugadores"}
    				msjJson = json.dumps(msj)
    				enviar(conexion, msjJson)
    			print("\n*Esperando jugadores*")
    			pass
    		elif pregunta == "si":
    			print("\n**Bienvenido a la fase de preguntas**")
    			break

    for i in lista_hilos_cliente:
    	i.start()
    aceptaRespuestas = True

    #Fase de preguntas		
    while True:
    	pregunta = input("¿Enviar pregunta? Ingrese si o no: ")
    	aceptaRespuestas = True
    	if pregunta == "si":
    		for x in lista_conexiones:
    			preg = {"mensaje": "pregunta", "valor": enviarPregunta(counter)}
    			pregJson = json.dumps(preg)
    			start_new_thread(enviar,(x, pregJson))
    		print("*Enviando pregunta*\n")
    		cancelarPregunta = input("Si desea cancelar la pregunta ingrese una 'c, de lo contrario cualquier otra letra': ")
    		while aceptaRespuestas == True:
    			if cancelarPregunta == "c":
    				for con in lista_conexiones:
    					msj = {"mensaje": "error", "valor": "Se ha cancelado la pregunta"}
    					msjJson = json.dumps(msj)
    					enviar(con, msjJson)
    					counter = counter + 1
    					aceptaRespuestas = False
    			pregunta = enviarPregunta(counter)
    			respuestaCorrecta, jugador = verificaRespuesta(pregunta)
    			if(respuestaCorrecta == True):
    				print("\nRespuesta correcta del jugador: " + str(jugador)) 
    				historial["Numero pregunta: " + str(counter), "Pregunta: "+ pregunta] = "Jugador con respuesta correcta: "+str(jugador) 				
    				counter = counter + 1
    				aceptaRespuestas = False
    			else:
    				pass

    	elif pregunta == "no":
    		print("\n***Partida terminada***")
    		print("***RANKING***\n")
    		print(mostrarRanking())
    		print("\n***HISTORIAL***\n")
    		print(mostrarHistorial())
    		g = ganador()
    		for x in lista_conexiones:
    			msj = {"mensaje": "ganador", "valor": "RANKING\n"+str(mostrarRanking()) + "\nHISTORIAL\n"+str(mostrarHistorial())}
    			msjJson = json.dumps(msj)
    			enviar(lista_conexiones[int(g)-1], msjJson)
    			if x != lista_conexiones[int(g)-1]:
    				msj = {"mensaje": "perdedor", "valor": "RANKING\n"+ str(mostrarRanking()) + "\nHISTORIAL\n"+str(mostrarHistorial())}
    				msjJson = json.dumps(msj)
    				enviar(x, msjJson)  			
    		break
    	else: 
    		print("La indicacion no es correcta.")
    		pass
    print("Cerrando conexiones.")
    s.close()

main()
