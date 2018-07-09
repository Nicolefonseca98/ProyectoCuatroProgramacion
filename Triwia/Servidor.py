from socket import *
from _thread import *
import time
import sys
import json

#Variables globales
bandera = False      	 #Utilizada en la desconexion/conexion de clientes
lista_de_clientes = []   #Lista de clientes que se conectan
lista_de_respuestas = {} #Lista de respuestas a evaluar
diccionario = {}		 #Diccionario que contiene las preguntas y sus respuestas
listaPreguntas = []
diccionarioMensajes = {}
listaConexiones = []

#Funciones
#Pide host y puerto
def ini():
    host = input("Host: ")
    port = int(input("Puerto: "))
    return host, port

#Crea un nuevo socket
def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

#Intenta ligar un socket con los parametros host y port
def ligarSocket(socket, host, port):
    while True:
        try:
            socket.bind((host, port))
            break
        except error as e:
            print("ERROR:", e)

#Espera por la conexión de clientes
def conexiones(socket):
    conn, addr = socket.accept()
    print("\nConexion Establecida.\nEl jugador es: ", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

#Llena diccionario con mensajes para enviar a los jugadores
def llenaDiccionarioMensajes():
	global diccionarioMensajes
	diccionarioMensajes['error'] = "Respuesta incorrecta"
	diccionarioMensajes['informacion'] = "Bienvenido"

#Envia un mensaje codificado a la direccion de los clientes
def enviar(conn, mensaje):
        # global diccionario
        # read = json.loads(open('preguntas.json').read())
        # for x in range(len(read)):
        #     diccionario[read[x]['enunciado']] = [read[x]['respuestas']]
        # for i in diccionario:
       	try:
       		conn.send(mensaje.encode("UTF-8"))
        except:
            print("\nNo se pudo enviar\n")
            print("Nuevo intento en 5 seg\n")
            time.sleep(5)

#Lee el archivo y llena el diccionario con la pregunta y su respuesta
# y una lista solo con las preguntas
def leerJson():
	global diccionario, listaPreguntas
	with open('preguntas.json') as preguntas:
		pregunta = json.load(preguntas)
		for x in pregunta:
			diccionario[x.get('enunciado')] = x.get('respuestas')
			listaPreguntas.append(x.get('enunciado'))

#Mensajes recibidos de los distintos clientes.
#Llama a la funcion cuando recibe mensajes de los clientes.
def recibir(conn):
	global bandera, lista_de_clientes
	print("hola")
	while True:
		try:
			reply = conn.recv(2048)
			reply = reply.decode("UTF-8")
			for x in lista_de_clientes:
				if reply[0] == str(x):
					print("Jugador ", reply)
					lista_de_respuestas[reply[0]] = reply[3: len(reply)]
					#start_new_thread(enviar, (conn,))
				else:
					bandera = True
					break
		except:
		   	print("No se pudo recibir respuesta")
		   	time.sleep(5)
	

#Verifica si en la lista se encuentra la respuesta correcta de la pregunta 
# que ingresa como parametro.
def verificaRespuesta(pregunta):
	mensaje = False
	global diccionario, lista_de_respuestas
	for x in diccionario:
		print(x, "soy x")
		if x == pregunta:
			for i in lista_de_respuestas:
				print(lista_de_respuestas[i],"Soy i")
				for y in diccionario[x]:
					print(y, "soy y")
					if lista_de_respuestas[i] == y:
						mensaje = True
					else:
						mensaje = False
	return mensaje
          
#El servidor asigna un numero a cada cliente y lo envia.
def enviarEspecial(conn, numeroCliente):
    global lista_de_clientes
    conn.send(str(numeroCliente).encode("UTF-8"))

#Método para enviar una pregunta a la vez a los jugadores
def enviarPregunta(counter):
	global listaPreguntas
	return listaPreguntas[counter]

#Método main
def main():
    global bandera, listaConexiones, listaPreguntas
    leerJson()
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(10)  
    counter = 0

    print("\nEsperando por los jugadores.")
    cantidadClientes = 1
    while True:
    	conn, addr = conexiones(s)
    	enviarEspecial(conn, cantidadClientes)
    	lista_de_clientes.append(str(cantidadClientes))
    	listaConexiones.append(conn)
    	print("Esperando jugadores")
    	cantidadClientes = cantidadClientes + 1
    	if len(lista_de_clientes) >= 2:
    		pregunta = input("¿Desea comenzar el juego? Ingrese si o no: ")
    		if pregunta == "no":
    			print("Esperando jugadores.")
    			pass
    		elif pregunta == "si":
    			print("Enviando pregunta")
    			for x in listaConexiones:
    				start_new_thread(enviar,(x, enviarPregunta(counter)))
    			print("Preguntas enviadas") 
    			if(verificaRespuesta(enviarPregunta(counter)) == True):
    				counter = counter + 1
    				print("Respuesta correcta")
    				pass
    	for i in listaConexiones:
    		start_new_thread(recibir, (i,))

    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
