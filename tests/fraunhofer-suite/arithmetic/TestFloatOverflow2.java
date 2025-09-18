 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestFloatOverflow2 {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     if (Double.MAX_VALUE * 2 == Double.POSITIVE_INFINITY) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }