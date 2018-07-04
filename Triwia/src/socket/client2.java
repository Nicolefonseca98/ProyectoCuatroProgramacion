
package socket;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

/**
 *
 * @author Nicole
 */
public class client2 {
    
    Boolean exit = false;
    String cliente = "";
    
    public String host() {
        System.out.println("host");
        Scanner sc = new Scanner(System.in);
        String host = sc.nextLine();
        return host;
    }
    
    public int port() {
        System.out.println("Port");
        Scanner sc = new Scanner(System.in);
        int port = sc.nextInt();
        return port;
    }
    
    public Socket creaSocket(String host, int port) throws IOException {
        Socket socket = new Socket(host, port);
        return socket;
    }
    
    public void enviar(Socket socket) throws IOException {
        //DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
        //dataOutputStream.writeUTF("1");
        PrintWriter pw = new PrintWriter(socket.getOutputStream());
        pw.println("1");
        pw.close();
        //socket.close();
    }

    public void recibir(Socket socket) throws IOException {
        //DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
        //System.out.println(dataInputStream.readUTF());
        BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        //while(true){
            String tmpRead = br.readLine();
            System.out.println("The result is: "+tmpRead);
        //}
        br.close();
    }
}
