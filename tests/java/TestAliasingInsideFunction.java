 package fraunhofer_suite.aliasing;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestAliasingInsideFunction {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String source = request.getHeader("Source");
     A a1 = new A();
     A a2 = new A();
     A b = foo4(a1);
     A c = bar4(a2);
     b.f = source;
     c.f = source;
     response.getWriter().println(a1.f);
     response.getWriter().println(a2.f);
   }

   class A {
     public String f;
   }

   A foo4(A p) {
     A a = p;
     A b = a;
     A c = b;
     return c;
   }

   A bar4(A p) {
     return new A();
   }
 }