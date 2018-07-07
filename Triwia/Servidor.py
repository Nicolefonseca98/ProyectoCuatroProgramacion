from socket import *
from _thread import *
import time
import sys
import json

#Variables globales
bandera = False      #Utilizada en la desconexion/conexion de clientes
lista_de_clientes = []  #El servidor le asigna un numero a los clientes según la lista
client = ""     # Numero del cliente

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
        diccionario = {}
        read = json.loads(open('preguntas.json').read())  
        for i in range(len(read)):
            diccionario[read[i]['enunciado']] = [read[i]['respuestas']]
        for i in diccionario:
            msg = i
       	try:
            conn.send(msg.encode("UTF-8"))
        except:
            print("\nNo se pudo enviar1\n")
            print("Nuevo intento en 5 seg\n")
            time.sleep(5)

#Mensajes recibidos de los distintos clientes.
#Llama a la funcion cuando recibe mensajes de los clientes.
def recibir(conn):
    while True:
        global bandera
        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")
            for x in lista_de_clientes:
                    print(x)  
                    if reply[0] == 1:
                        print("Jugador ", reply)
                        start_new_thread(enviar, (conn,))

            # elif reply[0] == "2":
            #     print("Jugador ", reply )
            #     start_new_thread(enviar, (conn,))
    
                #     else:
                # lista_de_clientes.append(reply[4])
                # print("\nEl jugador "+reply[4]+" se fue.")
                # bandera = True
                # break
        except:
            print("\nNo se pudo recibir respuesta.")
            print("Intento en 5 seg\n")
            time.sleep(5)
def prueba():
    for x in lista_de_clientes:
        print(x)


#El servidor asigna un numero a cada cliente y lo envia.
def enviarEspecial(conn):
    global lista_de_clientes,client
    client = lista_de_clientes.pop()
    conn.send(client.encode("UTF-8"))

#Método main
def main():
    global bandera
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(10)  

    print("\nEsperando por los jugadores.")

    cantidadClientes = 1
    while True: 
        lista_de_clientes.append(str(cantidadClientes))
        conn,addr = conexiones(s) 
        enviarEspecial(conn) # Espero conexion de los jugadores
        prueba()
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
