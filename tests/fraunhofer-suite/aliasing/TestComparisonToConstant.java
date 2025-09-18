 package fraunhofer_suite.aliasing;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestComparisonToConstant {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     A5 a1 = new A5(5);
     A5 a2 = new A5(7);

     if (foo5(a1, a2)) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }

     if (foo5(a1, a1)) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }
   }

   class A5 {
     public int f;

     public A5(int f) {
       this.f = f;
     }
   }

   boolean foo5(A5 p1, A5 p2) {
     p1.f = 5;
     return p2.f == 5;
   }
 }