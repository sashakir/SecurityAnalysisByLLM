 package fraunhofer_suite.virtual_dispatch;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestPassingPolymorphicValueToFunction1 {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Base var1 = new Derived1();
     Base var2 = new Derived2();

     foo1(response, var1, taint);
     foo2(response, var2, taint);
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

   private static void foo1(HttpServletResponse response, Base var, String taint) throws IOException {
     response.getWriter().println(var.foo(taint));
   }

   private static void foo2(HttpServletResponse response, Base var, String taint) throws IOException {
     response.getWriter().println(var.foo(taint));
   }
 }