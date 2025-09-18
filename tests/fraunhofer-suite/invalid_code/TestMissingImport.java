 package fraunhofer_suite.invalid_code;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 import static gov.fbi.Person.resolveAlias;

 public class TestMissingImport {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     String str = taint + resolveAlias("D.B. Cooper");
     response.getWriter().println(str);
   }
 }