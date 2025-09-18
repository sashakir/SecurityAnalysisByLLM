 package fraunhofer_suite.virtual_dispatch;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;


 public class TestFieldShadowing {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Derived1 var1 = new Derived1();
     var1.a = taint;
     response.getWriter().println(var1.getA());

     Base var2 = new Derived2();
     var2.a = taint;
     response.getWriter().println(var2.getA());
   }

   static class Base {
     public String a;
     String getA() {
       return a;
     }
   }

   static class Derived1 extends Base {
     public String a;
   }

   static class Derived2 extends Base {
   }
 }