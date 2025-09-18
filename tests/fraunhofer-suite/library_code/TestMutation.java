 package fraunhofer_suite.library_code;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.ArrayList;
 import static java.util.Collections.rotate;

 public class TestArrayItemReassignment {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     String a = taint;
     String b = "safe";

     ArrayList<String> arr = new ArrayList<>();
     arr.add(a);
     arr.add(b);
     arr.add(a);
     arr.add(b);

     rotate(arr, 1);

     response.getWriter().println(arr.get(1));
     response.getWriter().println(arr.get(2));
   }
 }