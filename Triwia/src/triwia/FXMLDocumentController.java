package triwia;

import java.io.IOException;
import java.net.Socket;
import java.net.URL;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import socket.Cliente;

/**
 *
 * @author Nicole Fonseca, Wilmer Mata.
 */
public class FXMLDocumentController implements Initializable {
    
    @FXML private AnchorPane anchorPane;
    @FXML private Label label;
    @FXML private TextField textFieldDireccionIp;
    @FXML private TextField textFieldPuerto;
    @FXML private Label labelPregunta;
    @FXML private TextArea textAreaRespuesta;
    @FXML private Label labelMensaje;
    @FXML private Label labelBienvenida;
    
    Socket socket;
    String numeroCliente;

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
        Cliente cliente = new Cliente();
        socket = cliente.creaSocket(textFieldDireccionIp.getText(), Integer.parseInt(textFieldPuerto.getText()));
        numeroCliente = cliente.recibir(socket);
        labelBienvenida.setText("Bienvenido jugador: " + numeroCliente);
        String pregunta = cliente.recibir(socket);
        labelPregunta.setText(pregunta);
    }
    
    @FXML
    private void buttonEnviarRespuesta(ActionEvent event) throws IOException {
        if (!textAreaRespuesta.getText().equals("")) {
            Cliente cliente = new Cliente();
            cliente.enviar(socket, numeroCliente + ": " + textAreaRespuesta.getText());
            String pregunta = cliente.recibir(socket);
            labelPregunta.setText(pregunta);
            textAreaRespuesta.setText("");
            labelMensaje.setText("Respuesta enviada.");
        } else {
            labelMensaje.setText("Debe escribir una respuesta.");
        }
    }
    
}
