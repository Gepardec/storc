package at.gepardec.demobatch;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class Hello {

    public static void main(String[] args) {
        System.out.println("Hello " + readProperty("myproperty"));
    }

    private static String readProperty( String key){
    	Properties prop = new Properties();
    	InputStream input = null;
    	
    	try {
        
    		String filename = "config.properties";
    		input = Hello.class.getClassLoader().getResourceAsStream(filename);
    		if(input==null){
    	            System.out.println("Sorry, unable to find " + filename);
    		    return "";
    		}
    		prop.load(input);
 
                return prop.getProperty(key);
 
    	} catch (IOException ex) {
    		ex.printStackTrace();
        } finally{
        	if(input!=null){
        		try {
				input.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
        	}
        }
        return "";
    }
}
