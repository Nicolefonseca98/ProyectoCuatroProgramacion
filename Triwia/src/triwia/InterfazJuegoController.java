
package triwia;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.layout.AnchorPane;

/**
 * FXML Controller class
 *
 * @author Nicole Fonseca, Wilmer Mata.
 */
public class InterfazJuegoController implements Initializable {

    @FXML private AnchorPane anchorPane;
    @FXML private TextArea textAreaRespuesta;
    @FXML private Label labelMensaje;

    /**
     * Initializes the controller class.
     * @param url
     * @param rb
     */
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
    private void buttonEnviar(ActionEvent event) {
        if (!textAreaRespuesta.getText().equals("")) {
            textAreaRespuesta.setText("");
            labelMensaje.setText("Respuesta enviada.");
        } else {
            labelMensaje.setText("Debe escribir una respuesta.");
        }

    }
    
}
