 package fraunhofer_suite.virtual_dispatch;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;


 public class TestFieldAccessViaLocalClass {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     response.getWriter().println(new Propagation1().foo(taint));
     response.getWriter().println(new Propagation2().foo(taint));
   }

   static class Propagation1 {
     String foo(String taint) {
       class B {
         String value = taint;
       }
       class C {
         String bar() {
           class C1 extends B {}
           B b = new C1();
           return b.value;
         }
       }
       return new C().bar();
     }
   }

   static class Propagation2 {
     String foo(String taint) {
       class B {
         String value = taint;
       }
       class C {
         String bar() {
           class C1 extends B {
             String value = "safe";
           }
           C1 b = new C1();
           return b.value;
         }
       }
       return new C().bar();
     }
   }
 }