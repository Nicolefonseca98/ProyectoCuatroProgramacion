
package socket;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Reader;
import java.net.Socket;
import java.util.Scanner;

/**
 *
 * @author Nicole
 */
public class Cliente {
    
    Boolean exit = false;
    String cliente = "";
    
//    public String host() {
//        System.out.println("host");
//        Scanner sc = new Scanner(System.in);
//        String host = sc.nextLine();
//        return host;
//    }
//    
//    public int port() {
//        System.out.println("Port");
//        Scanner sc = new Scanner(System.in);
//        int port = sc.nextInt();
//        return port;
//    }
    
    public Socket creaSocket(String host, int port) throws IOException {
        Socket socket = new Socket(host, port);
        return socket;
    }
    
    public void enviar(Socket socket) throws IOException {
//        PrintWriter printWriter = new PrintWriter(socket.getOutputStream());
//        printWriter.println("1 hola");
       BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
       bufferedWriter.write("1 hola");
       bufferedWriter.flush();
//        printWriter.flush();
       
    }

    public void recibir(Socket socket) throws IOException {
        InputStreamReader inputStreamReader = new InputStreamReader(socket.getInputStream());
        BufferedReader br = new BufferedReader(inputStreamReader);
        StringBuilder sb = new StringBuilder();
        String str;
        while((str = br.readLine()) != null) {
            sb.append(str + "\n");
            System.out.println("The result is: "+str);
        }
        br.close();
    }
}
