
package triwia;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;

/**
 *
 * @author Nicole Fonseca, Wilmer Mata.
 */
public class FXMLDocumentController implements Initializable {
  
    @FXML private AnchorPane anchorPane;
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        //Fondo de la ventana
        String backgroundImage = "/imagenes/FondoLejos.png";
        anchorPane.setStyle("-fx-background-image: url('" + backgroundImage + "'); "
                + "-fx-background-position: left top, center;"
                + "-fx-background-repeat: no-repeat;"
                + "-fx-background-size: cover, auto;");
    }    

    @FXML
    private void empezarJuego(ActionEvent event) throws IOException {     
        Parent parent = FXMLLoader.load(getClass().getResource("InterfazJuego.fxml"));
        Scene scene = new Scene(parent);
        Stage window = (Stage) ((Node) event.getSource()).getScene().getWindow();
        window.setTitle("Jugar");
        window.setScene(scene);
        window.show();
    }
    
}
