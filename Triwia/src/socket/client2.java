
package socket;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Nicole
 */
public class client2 {
    
    Boolean exit = false;
    String cliente = "";
    
    public String host() {
        Scanner sc = new Scanner(System.in);
        String host = sc.nextLine();
        return host;
    }
    
    public int port() {
        Scanner sc = new Scanner(System.in);
        int port = sc.nextInt();
        return port;
    }
    
    public Socket creaSocket() throws IOException {
        Socket socket = new Socket(host(), port());
        return socket;
    }
    
    public void conectar() throws IOException {
        creaSocket().connect(creaSocket().getLocalSocketAddress());
    }
    
    public void intentoConexion() throws InterruptedException {
        while (true) {
            System.out.println("\nTrying to connect to:" + host() + ":" + port());
            try {
                conectar();
            } catch (IOException ex) {
                System.out.println("Trying again in 5 Seconds\n");
                Thread.sleep(5000);
            }
        }

    }
    
    String mensaje;
    public void enviar (Socket socket) throws IOException {
        
        while (true) {
            if(exit) {
                Scanner sc = new Scanner(System.in);
                 mensaje = sc.nextLine();
                mensaje = cliente +": " + mensaje;
                if(mensaje == cliente+": salir") {
                    exit = true;
                    mensaje = "The "+cliente+" Client is gone";
                    DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
                    dataOutputStream.write(mensaje.getBytes());
                    socket.close();
                } else { 
                    Thread t = new Thread(new Runnable() {
                        public void run() {
                            try {
                                DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
                                dataOutputStream.write(mensaje.getBytes());
                            } catch (IOException ex) {
                                Logger.getLogger(client2.class.getName()).log(Level.SEVERE, null, ex);
                            }
                        }
                    });
                    t.start();
                }

            }
        }
    }
    

}
