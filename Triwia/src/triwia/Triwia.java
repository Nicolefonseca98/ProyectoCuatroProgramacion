
package triwia;

import java.io.IOException;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import socket.client2;

/**
 *
 * @author Nicole Fonseca, Wilmer Mata.
 */
public class Triwia extends Application {
    
    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("FXMLDocument.fxml"));
        
        Scene scene = new Scene(root);
        
        stage.setScene(scene);
        stage.setTitle("Bienvenida");
        stage.show();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        //launch(args);
        client2 c = new client2();
        try {
            Socket s = c.creaSocket();
            c.intentoConexion();
//            c.enviar(s);
            System.out.println("conexión");
            
        } catch (IOException ex) {
            Logger.getLogger(Triwia.class.getName()).log(Level.SEVERE, null, ex);
        } catch (InterruptedException ex) {
            Logger.getLogger(Triwia.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}
