
package triwia;

import java.io.IOException;
import java.net.Socket;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import socket.Cliente;

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
    public static void main(String[] args) throws IOException {

        launch(args);
//        Cliente c = new Cliente();
//        Socket s = c.creaSocket("localhost", 5000);
//        c.recibir(s);
//        c.enviar(s, "1hola");
//        c.recibir(s);
    }
    
}
