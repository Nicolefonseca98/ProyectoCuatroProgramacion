
package json;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author Nicole Fonseca, Wilmer Mata.
 */
public class leerJson {
    
    public void leer() throws ParseException {
        JSONObject jsonObject = (JSONObject) new JSONParser().parse("{\"name\": \"John\"}");
        System.out.println(jsonObject.get("name"));
    }
}
