 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestOverflow {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     if (Integer.MAX_VALUE + 1 == Integer.MIN_VALUE) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }