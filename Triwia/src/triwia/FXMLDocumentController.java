package triwia;

import java.io.IOException;
import java.net.Socket;
import java.net.URL;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import socket.Cliente;

/**
 *
 * @author Nicole Fonseca, Wilmer Mata.
 */
public class FXMLDocumentController implements Initializable {

    @FXML
    private AnchorPane anchorPane;
    @FXML
    private Label label;
    @FXML
    private TextField textFieldDireccionIp;
    @FXML
    private TextField textFieldPuerto;
    @FXML
    private Label labelPregunta;
    @FXML
    private TextArea textAreaRespuesta;
    @FXML
    private Label labelMensaje;
    @FXML
    private Label labelBienvenida;

    Socket socket;
    String numeroCliente;
    public static String ranking;

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        //Fondo de la ventana
        String backgroundImage = "/imagenes/FondoLejos.png";
        anchorPane.setStyle("-fx-background-image: url('" + backgroundImage + "'); "
                + "-fx-background-position: left top, center;"
                + "-fx-background-repeat: no-repeat;"
                + "-fx-background-size: cover, auto;");
    }
    String pregunta;
    char num;

    @FXML
    private void empezarJuego(ActionEvent event) throws IOException, ParseException {
        try {
            Cliente cliente = new Cliente();
            socket = cliente.creaSocket(textFieldDireccionIp.getText(), Integer.parseInt(textFieldPuerto.getText()));
            numeroCliente = cliente.recibir(socket);
            num = numeroCliente.charAt(numeroCliente.length() - 3);
            labelBienvenida.setText(jsonParser(numeroCliente));
            new Thread(new Runnable() {
                @Override
                public void run() {
                    while (true) {
                        try {
                            pregunta = cliente.recibir(socket);
                            Platform.runLater(new Runnable() {
                                @Override
                                public void run() {
                                    try {
                                        String rankingString = jsonParserRanking(pregunta);
                                        String preg = jsonParser(pregunta);
                                        labelPregunta.setText(jsonParser(pregunta));
                                        labelMensaje.setText("");
                                        try {
                                            if (rankingString.equalsIgnoreCase("ganador")) {
                                                ranking = preg;
                                                cambioScene("Ganador.fxml");
                                            } else if (rankingString.equalsIgnoreCase("perdedor")) {

                                                ranking = preg;
                                                cambioScene("Perdedor.fxml");

                                            }
                                        } catch (NullPointerException | IOException npe) {
                                        }
                                    } catch (ParseException ex) {
                                    }
                                }
                            });

                        } catch (IOException ex) {
                        }
                    }
                }
            }).start();
        } catch (Exception exception) {
        }
    }

    @FXML
    private void buttonEnviarRespuesta(ActionEvent event) throws IOException {
        if (!textAreaRespuesta.getText().equals("")) {
            Cliente cliente = new Cliente();
            cliente.enviar(socket, num + ": " + textAreaRespuesta.getText());
            textAreaRespuesta.setText("");
            labelMensaje.setText("Respuesta enviada.");
        } else {
            labelMensaje.setText("Debe escribir una respuesta.");
        }
    }

    public String jsonParser(String mensaje) throws ParseException {
        JSONParser parser = new JSONParser();
        JSONObject json = (JSONObject) parser.parse(mensaje);
        String mensajeJson = (String) json.get("valor");
        return mensajeJson;
    }

    public String jsonParserRanking(String mensaje) throws ParseException {
        JSONParser parser = new JSONParser();
        JSONObject json = (JSONObject) parser.parse(mensaje);
        String mensajeJson = (String) json.get("mensaje");
        return mensajeJson;
    }

    private void cambioScene(String destino) throws IOException {
        Parent tableViewParent = FXMLLoader.load(getClass().getResource(destino));
        Scene tableViewScene = new Scene(tableViewParent);
        //Esta linea obtiene la informacion del Stage
        Stage window = (Stage) ((Node) anchorPane).getScene().getWindow();

        window.setScene(tableViewScene);
        window.setResizable(false);
        window.setX(0);
        window.setY(0);
        window.setFullScreen(false);
        window.show();

    }

}
