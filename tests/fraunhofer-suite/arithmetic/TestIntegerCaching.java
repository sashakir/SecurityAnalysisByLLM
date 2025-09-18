 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestIntegerCaching {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");

     Integer x1 = 127;
     Integer x2 = 127;
     Integer y1 = 128;
     Integer y2 = 128;

     if (x1 == x2) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }

     if (y1 == y2) {
       response.getWriter().println(taint);
     } else {
       response.getWriter().println(taint);
     }
   }
 }