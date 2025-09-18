 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestFloatUnderflow {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     if (Math.pow(2, -1075) == 0.0) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }