
package socket;

import java.io.BufferedInputStream;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;

/**
 *
 * @author Nicole Fonseca Wilmer Mata.
 */
public class Cliente {
    
    Boolean exit = false;
    String cliente = "";
    
    public Socket creaSocket(String host, int port) throws IOException {
        Socket socket = new Socket(host, port);
        return socket;
    }
    
    public void enviar(Socket socket, String mensaje) throws IOException {
       BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
       bufferedWriter.write(mensaje);
       bufferedWriter.flush();
    }

    public String recibir(Socket socket) throws IOException {
        DataInputStream in = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
        byte[] bytes = new byte[1024];
        in.read(bytes);
        String reply = new String(bytes, "UTF-8");
        return reply.trim();
    }
}
