from socket import *
from _thread import *
import time
import sys
import json
import threading

#Variables globales
bandera = False      	 		#Utilizada en la desconexion/conexion de clientes.
aceptaConexiones = True  		#Acepta conexiones de los clientes.
lista_de_clientes = []   		#Lista de clientes que se conectan, guarda el numero del cliente.
diccionario_de_respuestas = {}  #Lista de respuestas a evaluar, se guarda el numero del cliente y la respuesta.
diccionario = {}		 		#Diccionario que contiene las preguntas y sus respuestas.
lista_preguntas = []			#Lista con las preguntas a realizar.
diccionario_mensajes = {}		#Diccionario que contiene los diferentes mensajes para enviar al cliente.
lista_conexiones = []			#Guarda la conexion de cada cliente.
lista_hilos_cliente = []		#Guarda el hilo de cada cliente para empezar a recibir respuestas.
historial = {}					#Guarda las respuestas correctas e incorrectas de cada cliente para mostrar un historial
								# al final de cada partida.

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
            print("No se puede conectar.")

#Espera por la conexión de clientes
def conexiones(socket):
    conn, addr = socket.accept()
    print("\nConexion Establecida.\nEl jugador es: ", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

#Llena diccionario con mensajes para enviar a los jugadores
def llenaDiccionarioMensajes():
	global diccionario_mensajes
	diccionario_mensajes['error'] = "Respuesta incorrecta"
	diccionario_mensajes['informacion'] = "Bienvenido"

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
	global diccionario, lista_preguntas
	with open('preguntas.json') as preguntas:
		pregunta = json.load(preguntas)
		for x in pregunta:
			diccionario[x.get('enunciado')] = x.get('respuestas')
			lista_preguntas.append(x.get('enunciado'))

#Mensajes recibidos de los distintos clientes.
#Llama a la funcion cuando recibe mensajes de los clientes.
def recibir(conn):
	global bandera, lista_de_clientes
	while True:
		try:
			reply = conn.recv(2048)
			reply = reply.decode("UTF-8")
			for x in lista_de_clientes:
				if reply[0] == str(x):
					print("Jugador ", reply)
					diccionario_de_respuestas[reply[0]] = reply[3: len(reply)]
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
	global diccionario, diccionario_de_respuestas, historial
	for x in diccionario:
		if x == pregunta:
			for i in diccionario_de_respuestas:
				for y in diccionario[x]:
					if diccionario_de_respuestas[i] == y:
						historial[i] = "Respuesta correcta" 
						mensaje = True
					else:
						historial['Jugador ',i] = "Respuesta incorrecta"
						mensaje = False
	return mensaje
          
#El servidor asigna un numero a cada cliente y lo envia.
def enviarNumeroJugador(conn, numeroCliente):
    global lista_de_clientes
    conn.send(str(numeroCliente).encode("UTF-8"))

#Método para enviar una pregunta a la vez a los jugadores
def enviarPregunta(counter):
	global lista_preguntas
	return lista_preguntas[counter]

def iniciarHilos():
	global  lista_hilos_cliente
	for x in lista_hilos_cliente:
		x.start()

#Método main
def main():
    global bandera, lista_conexiones, lista_preguntas, lista_hilos_cliente, aceptaConexiones
    leerJson()
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(10)  
    counter = 0

    print("\nFase de conexiones.","\nEsperando por los jugadores.")
    cantidadClientes = 1
    #Fase de conexiones
    while aceptaConexiones == True:
    	conn, addr = conexiones(s)
    	enviarNumeroJugador(conn, cantidadClientes)
    	lista_de_clientes.append(str(cantidadClientes))
    	lista_conexiones.append(conn)
    	
    	print("Esperando jugadores")
    	cantidadClientes = cantidadClientes + 1
    	if len(lista_de_clientes) >= 2:
    		pregunta = input("¿Desea comenzar el juego? Ingrese si o no: ")
    		if pregunta == "no":
    			print("Esperando jugadores.")
    			pass
    		elif pregunta == "si":
    			print("Bienvenido a la fase de preguntas")
    			break
    			

    #Fase de preguntas		
    while True:
    	pregunta = input("¿Enviar pregunta? Ingrese si o no: ")
    	if pregunta == "si":
    		for x in lista_conexiones:
    			start_new_thread(enviar,(x, enviarPregunta(counter)))
    			hilo = threading.Thread()
    			lista_hilos_cliente.append(hilo)
    		iniciarHilos()
    		if(verificaRespuesta(enviarPregunta(counter)) == True):
    			counter = counter + 1
    			print("Respuesta correcta")
    			pass
    	elif pregunta == "no":
    		pass
    	else: 
    		print("La indicacion no es correcta")
    		break


    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False

main()
