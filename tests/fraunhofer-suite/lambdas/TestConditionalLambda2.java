 package fraunhofer_suite.lambdas;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.function.Function;

 public class TestConditionalLambda2 {
   public static void test(HttpServletRequest request, HttpServletResponse response, boolean condition) throws IOException {
     String taint = request.getHeader("value");
     String a = taint;

     Function<String, String> f1 = (x) -> x;
     Function<String, String> f2 = (x) -> x.equals(taint) ? "safe" : taint;
     Function<String, String> f = condition ? f1 : f2;

     String b = f.apply(a);
     response.getWriter().println(b);
   }
 }