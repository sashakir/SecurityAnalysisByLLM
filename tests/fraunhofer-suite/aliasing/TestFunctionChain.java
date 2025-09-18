 package fraunhofer_suite.aliasing;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestFunctionChain {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     String x = f1(taint);
     String y = f1("safe");
     response.getWriter().println(x);
     response.getWriter().println(y);
   }

   String f1(String s) { return f2(s); }
   String f2(String s) { return f3(s); }
   String f3(String s) { return f4(s); }
   String f4(String s) { return f5(s); }
   String f5(String s) { return f6(s); }
   String f6(String s) { return f7(s); }
   String f7(String s) { return f8(s); }
   String f8(String s) { return f9(s); }
   String f9(String s) { return f10(s); }
   String f10(String s) { return f11(s); }
   String f11(String s) { return f12(s); }
   String f12(String s) { return f13(s); }
   String f13(String s) { return f14(s); }
   String f14(String s) { return f15(s); }
   String f15(String s) { return s; }
 }