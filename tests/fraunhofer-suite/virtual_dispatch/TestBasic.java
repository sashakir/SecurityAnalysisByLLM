 package fraunhofer_suite.virtual_dispatch;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;


 public class TestBasic {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Base var1 = new Derived1();
     Base var2 = new Derived2();

     response.getWriter().println(var1.foo(taint));
     response.getWriter().println(var2.foo(taint));
   }

   static class Base {
     String foo(String str) {
       return "Base";
     }
   }

   static class Derived1 extends Base {
     @Override
     String foo(String str) {
       return "Derived1";
     }
   }

   static class Derived2 extends Base {
     @Override
     String foo(String str) {
       return str;
     }
   }
 }