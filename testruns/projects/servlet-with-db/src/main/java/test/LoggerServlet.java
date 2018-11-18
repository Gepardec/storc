package test;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

@WebServlet(urlPatterns="/hello")
public class LoggerServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    static Log log = LogFactory.getLog(LoggerServlet.class);
    
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
	    throws ServletException, IOException {
	response.setContentType("text/html");
	PrintWriter out = response.getWriter();
	out.println("<html><head><title>Logger Service</title></head><body>");
	out.println("Start<br/>");
	out.println(new Date().toString() + "<br/>");

	out.println("Ich schreibe Log-Einträge mit der Kategorie 'test.LoggerServlet'.<br/>");
	out.println("Error<br/>");
	log.error("Dies ist eine Error-Message");
	out.println("Warnung<br/>");
	log.warn("Dies ist eine Warnung-Message");
	out.println("Info<br/>");
	log.info("Dies ist eine Info-Message");
	out.println("Debug<br/>");
	log.debug("Dies ist eine Debug-Message");
	out.println("Trace<br/>");
	log.trace("Dies ist eine Trace-Message");

	out.println("End<br/>");
	out.println("</body>");
	out.println("</html>");
    }
}