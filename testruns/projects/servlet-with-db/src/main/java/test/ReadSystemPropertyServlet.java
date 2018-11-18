package test;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.URL;
import java.util.Date;
import java.util.Properties;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

@WebServlet(urlPatterns = "/systemproperty")
public class ReadSystemPropertyServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	static Log log = LogFactory.getLog(ReadSystemPropertyServlet.class);

	@Override
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("text/html");
		PrintWriter out = response.getWriter();
		out.println("<html><head><title>Property Service</title></head><body>");
		out.println("Start<br/>");
		out.println(new Date().toString() + "<br/>");

		out.println("Lese System Property 'myTestProperty'.<br/>");
		out.println("Value: " + readProperty() + "<br/>");

		out.println("End<br/>");
		out.println("</body>");
		out.println("</html>");
	}

	private String readProperty() {

		Properties prop = new Properties();
		try {
			prop.load(this.getClass().getResourceAsStream("/mytest.properties"));
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
		return prop.getProperty("myTestProperty", "Nicht gefunden");
	}
}