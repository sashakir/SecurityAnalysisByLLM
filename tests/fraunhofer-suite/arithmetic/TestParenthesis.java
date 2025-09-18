 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestParenthesis {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     if (2 * (1 + 1) == 4) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }