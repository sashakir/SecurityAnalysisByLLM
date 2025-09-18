 package fraunhofer_suite.conditions;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestConstantExpressionWithObject {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");

     if (filter(new B5(new A5(7)), 8)) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }
   }

   class A5 {
     int x;

     public A5(int x) {
       this.x = x;
     }
   }

   class B5 {
     A5 y;

     public B5(A5 y) {
       this.y = y;
     }
   }

   private boolean filter(B5 param1, int param2) {
     return param1.y.x > param2;
   }
 }