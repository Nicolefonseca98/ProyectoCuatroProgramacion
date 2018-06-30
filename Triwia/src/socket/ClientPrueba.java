/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package socket;

import java.net.*; //Biblioteca de funciones de red
import java.io.*; // Biblioteca de manejo de flujos
/**
 *
 * @author Wilmata
 */
public class ClientPrueba {
    
    public static void main(String[] args) throws Exception{
        byte [] datos = new byte[256]; //Buffer de datps recibidos
//        String dirIP;  //Variable que almacena la IP del servidor
        String msg = "Hola soy un cliente de Java\n"; //Mensaje a enviar
        System.out.println("Escriba la direccion IP a conectarse: ");
        BufferedReader x = new BufferedReader(new InputStreamReader(System.in)); //habilita la entrada del teclado
//        dirIP = x.readLine(); //Pedir la direcciòn IP del servidor
//        Socket socket = new Socket(dirIP,5000); //Inicializar la comunicacion en el puerto 5000
 Socket socket = new Socket("localHost",5000); //Inicializar la comunicacion en el puerto 5000        
DataInputStream din = new DataInputStream(socket.getInputStream()); //Habilita el flujo de entrada del socket
        
        DataOutputStream dos = new DataOutputStream(socket.getOutputStream()); //Habilita el flujo de salidad del socket
        
        System.out.println("Enviando un mensaje al servidor: "+ msg);
        dos.write(msg.getBytes()); //Enviar el mensaje al servidor en bytes
        dos.flush();
        din.read(datos,0,datos.length); //Leer el mensaje del servidor
        String message = new String(datos);//Convertir a cadena el mensaje recibido
        System.out.println(message); //Imprimir el mensaje del servidor
        din.close();//Cerrar flujo de entrada
        dos.close(); //y salida del socket
        socket.close(); // cerrar el socket y finalizar la comunicacion
    }
}
