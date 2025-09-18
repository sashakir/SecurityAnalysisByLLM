 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestUnderflow {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     if (Integer.MIN_VALUE - 1 == Integer.MAX_VALUE) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }