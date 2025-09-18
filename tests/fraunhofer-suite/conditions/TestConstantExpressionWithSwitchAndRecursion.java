 package fraunhofer_suite.conditions;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestConstantExpressionWithSwitchAndRecursion {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");

     if (filter(0)) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }
   }

   private int foo(int param) {
     switch (param) {
       case 0:
         return 2;
       case 1:
         return 3;
       case 2:
         return 5;
       case 3:
         return 8;
       default:
         return 13;
     }
   }

   private boolean filter(int param) {
     return foo(foo(param)) == 5;
   }
 }