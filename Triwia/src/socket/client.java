package socket;

/**
 *
 * @author Wilmer Mata Nicole Fonseca
 */
import java.io.*;
import java.net.*;
import java.lang.*;
import javax.swing.JOptionPane;

public class client {

    public static void main(String[] args) {

        try {
            Socket socket = new Socket("localhost", 4000);

            DataOutputStream dout = new DataOutputStream(socket.getOutputStream());
            DataInputStream din = new DataInputStream(socket.getInputStream());
            String message = JOptionPane.showInputDialog(null, "Ingrese algo");
            dout.writeUTF(message);
            dout.flush();

            System.out.println("send first mess");
            String str = din.readUTF();//in.readLine();

            System.out.println("Message" + str);

            dout.close();
            din.close();
            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
