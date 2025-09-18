 package fraunhofer_suite.virtual_dispatch;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;


 public class TestFieldAccessViaInnerClass {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Base var1 = new Base();
     var1.a = taint;
     response.getWriter().println(var1.getFieldViaInner());
     var1.a = "safe";
     response.getWriter().println(var1.getFieldViaInner());
   }

   static class Base {
     public String a;
     public String getFieldViaInner() {
       return new Inner1().getA();
     }
     class Inner1 {
       String getA() {
         return a;
       }
     }
   }
 }