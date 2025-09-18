 package fraunhofer_suite.arithmetic;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestUnknownValue {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition, int x) throws IOException {
     String taint = request.getHeader("value");
     String a = taint;
     String b = "safe";

     if (x > 0) {
       b = a;
     }

     response.getWriter().println(b);
   }
 }