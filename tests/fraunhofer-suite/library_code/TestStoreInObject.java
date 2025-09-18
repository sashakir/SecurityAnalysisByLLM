 package fraunhofer_suite.library_code;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.lang.StringBuilder;

 public class TestStoreInObject {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     StringBuilder sb = new StringBuilder();
     sb.append(taint);

     response.getWriter().println(sb.toString());
   }
 }