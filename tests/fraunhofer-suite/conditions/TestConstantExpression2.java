 package fraunhofer_suite.conditions;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestConstantExpression2 {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");

     if (filter(8, 7)) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }
   }

   private boolean filter(int param1, int param2) {
     return param1 > param2;
   }
 }