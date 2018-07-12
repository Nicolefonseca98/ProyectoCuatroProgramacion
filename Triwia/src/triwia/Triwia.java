
package triwia;

import java.io.IOException;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

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
        stage.setTitle("Triwia");
        stage.getIcons().add(new Image("/imagenes/signo.png")); 
        stage.show();
        stage.setOnCloseRequest(e -> {
        Platform.exit();
        System.exit(0);
    });

    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {

        launch(args);
    }
    
}
