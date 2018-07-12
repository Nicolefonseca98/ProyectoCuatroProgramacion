
package triwia;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.animation.PathTransition;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.shape.Line;
import javafx.util.Duration;
import static triwia.FXMLDocumentController.ranking;

/**
 *
 * @author Nicole Fonseca, Wilmer Mata
 */
public class PerdedorController implements Initializable {

    @FXML
    private ImageView textoImageView;
    @FXML
    private ImageView gif1ImageView;
    @FXML
    private ImageView gif2ImageView;
    @FXML
    private Label rankingLabel;

    /**
     * Initializes the controller class.
     */
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        Image texto = new Image("/imagenes/perdedor.gif");
        textoImageView.setImage(texto);
        Image gif1 = new Image("/imagenes/rick3.gif");
        gif1ImageView.setImage(gif1);
        Image gif2 = new Image("/imagenes/rick2.gif");
        gif2ImageView.setImage(gif2);
        rankingLabel.setText(ranking);
        Line line = new Line(-300, 20, 800, 20);
        PathTransition transition = new PathTransition();
        transition.setNode(textoImageView);
        transition.setDuration(Duration.seconds(4));
        transition.setPath(line);
        transition.setCycleCount(PathTransition.INDEFINITE);
        transition.play();
    }

}
