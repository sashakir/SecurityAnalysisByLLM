 package fraunhofer_suite.maps;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.HashMap;
 import java.util.Map;

 public class TestMapItemReassignment {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     String a = taint;
     String b = "safe";

     Map<Integer, String> map = new HashMap<>();
     map.put(1, a);
     map.put(2, b);
     map.put(3, map.get(1));

     response.getWriter().println(map.get(3));
   }
 }