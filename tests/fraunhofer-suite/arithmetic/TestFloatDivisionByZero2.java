 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestFloatDivisionByZero2 {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     if (1/-0.0 == Double.NEGATIVE_INFINITY) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }