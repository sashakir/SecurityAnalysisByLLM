 package fraunhofer_suite.taint_sources;

 import org.springframework.web.bind.annotation.RequestParam;
 import javax.servlet.http.HttpServlet;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class RequestParamObject extends HttpServlet {
   public void test(@RequestParam UserData taint, HttpServletResponse response) throws IOException {
     response.getWriter().println(taint.value);
   }

   class UserData {
     public String value;
   }
 }