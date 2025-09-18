 package fraunhofer_suite.virtual_dispatch;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestPassingPolymorphicValueToFunction2 {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Base var1 = new Derived1();
     Base var2 = new Derived2();

     foo1(response, var1, "safe");
     foo2(response, var2, taint);
   }

   static class Base {
     void print(HttpServletResponse response, String str) throws IOException {
       System.out.println(str);
     }
   }

   static class Derived1 extends Base {
     @Override
     void print(HttpServletResponse response, String str) throws IOException {
       response.getWriter().println(str);
     }
   }

   static class Derived2 extends Base {
     @Override
     void print(HttpServletResponse response, String str) throws IOException {
       response.getWriter().println(str);
     }
   }

   private static void foo1(HttpServletResponse response, Base var, String taint) throws IOException {
     var.print(response, taint);
   }

   private static void foo2(HttpServletResponse response, Base var, String taint) throws IOException {
     var.print(response, taint);
   }
 }