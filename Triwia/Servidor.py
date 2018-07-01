from socket import *
from _thread import *
import time
import sys

#Funciones
#Pide host y puerto
def ini():
    host = input("Host: ")
    port = int(input("Port: "))
    return host, port

#Crea un nuevo socket
def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

#Intenta ligar un socket con los parametros host y port
def ligarSocket(s, host, port):
    while True:
        try:
            s.bind((host, port))
            break

        except error as e:
            print("ERROR:", e)

#Espera por la conexión de clientes
def conexiones(s):

    conn, addr = s.accept()
    print("\nEstablished Connection.\nThe client is:", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

#Envia un mensaje codificado a la direccion del cliente 1
def enviar(conn):

        msg = input("")
        msg = "Servidor: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happend")
            print("Try in 5 seg\n")
            time.sleep(5)

#Envia un mensaje codificado a la direccion del cliente 2.
def enviar2(conn):

        msg = input("")
        msg = "Servidor: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happend")
            print("Try in 5 seg\n")
            time.sleep(5)

#Mensajes recibidos de los distintos clientes.
#Llama a la funcion cuando recibe mensajes de los clientes.
def recibir(conn):
    while True:
        global bandera
        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")

            if reply[0] == "1":
                print("Cliente", reply)
                start_new_thread(enviar, (conn,))

            elif reply[0] == "2":
                print("Cliente", reply)
                start_new_thread(enviar2, (conn,))

            else:
                lista_de_clientes.append(reply[4])
                print("\nThe client "+reply[4]+" is gone")
                bandera = True
                break



        except:
            print("\nCant recieve response")
            print("Trying in 5 seg\n")
            time.sleep(5)


#El servidor asigna un numero a cada cliente y lo envia.
def enviarEspecial(conn):
    global lista_de_clientes,client
    client = lista_de_clientes.pop()
    conn.send(client.encode("UTF-8"))

#Variables globales
bandera = False      #Utilizada en la desconexion/conexion de clientes
lista_de_clientes = ["2","1"]   #El servidor le asigna un numero a los
                                #clientes segun esta lista
client = ""     # Numero del cliente


#Método main
def main():

    global bandera
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(2)     # Espero 2 clientes

    print("\nW A R N I N G : THE SERVER IS A SLAVE. DON'T "
          "WRITE IF THE SERVER DOESN'T HAVE ANY MESSAGE TO RESPONSE")
    print("\nWaiting for clients")

    conn,addr = conexiones(s)
    enviarEspecial(conn)               # Espero conexion del 1 cliente
    start_new_thread(recibir,(conn,))

    conn2,addr2 = conexiones(s)
    enviarEspecial(conn2)              # Espero conexion del 2 cliente
    start_new_thread(recibir,(conn2,))

    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
