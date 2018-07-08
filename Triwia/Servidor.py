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
lista = []
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

#Envia un mensaje codificado a la direccion de los clientes
def enviar(conn):
        # global diccionario
        # read = json.loads(open('preguntas.json').read())
        # for x in range(len(read)):
        #     diccionario[read[x]['enunciado']] = [read[x]['respuestas']]
        # for i in diccionario:
        msg = leerJson()
        mensaje = verificaRespuesta(msg)
        conn.send(mensaje.encode("UTF-8"))
       	try:
       		pregunta = input("¿Desea enviar una pregunta? Ingrese si o no: ")
       		if pregunta == "si":
       			print("Ya no se aceptan más jugadores")
       			conn.send(msg.encode("UTF-8"))
       		elif pregunta == "no":
       			print("Esperando jugadores")
       			conn.send("Esperando jugadores".encode("UTF-8"))
        except:
            print("\nNo se pudo enviar1\n")
            print("Nuevo intento en 5 seg\n")
            time.sleep(5)

def leerJson():
	global diccionario
	with open('preguntas.json') as preguntas:
		pregunta = json.load(preguntas)
		for x in pregunta:
			diccionario[x.get('enunciado')] = x.get('respuestas')
			lista.append(x.get('enunciado'))
			return lista.pop()

#Mensajes recibidos de los distintos clientes.
#Llama a la funcion cuando recibe mensajes de los clientes.
def recibir(conn):
    while True:
        global bandera, lista_de_clientes
        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")
            for x in (lista_de_clientes):
                    if reply[0] == str(x):
                        print("Jugador ", reply)
                        lista_de_respuestas[reply[0]] = reply[3:len(reply)]
                        start_new_thread(enviar, (conn,))
                    else:
                    	bandera = True
                    	break
        except:
            print("\nNo se pudo recibir respuesta.")
            print("Intento en 5 seg\n")
            time.sleep(5)

#Verifica si en la lista se encuentra la respuesta correcta de la pregunta 
# que ingresa como parametro.
def verificaRespuesta(pregunta):
	mensaje = ""
	global diccionario, lista_de_respuestas
	for x in diccionario:
		print(x, "soy x")
		if x == pregunta:
			for i in lista_de_respuestas:
				print(lista_de_respuestas[i],"Soy i")
				for y in diccionario[x]:
					print(y, "soy y")
					if lista_de_respuestas[i] == y:
						mensaje = "Respuesta correcta"
					else:
						mensaje = "Respuesta incorrecta"
	return mensaje
          
#El servidor asigna un numero a cada cliente y lo envia.
def enviarEspecial(conn, numeroCliente):
    global lista_de_clientes
    conn.send(str(numeroCliente).encode("UTF-8"))

#Método main
def main():
    global bandera
    leerJson()
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(10)  

    print("\nEsperando por los jugadores.")
    cantidadClientes = 1
    while True:
    	conn, addr = conexiones(s)
    	lista_de_clientes.append(str(cantidadClientes))
    	enviarEspecial(conn, cantidadClientes)
    	cantidadClientes = cantidadClientes + 1
    	start_new_thread(enviar,(conn,))
    	start_new_thread(recibir,(conn,)) 
    
    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
