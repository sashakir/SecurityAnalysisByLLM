 package fraunhofer_suite.maps;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.HashMap;
 import java.util.Map;

 public class TestBasic {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Map<String, String> map = new HashMap();
     map.put("key1", "good");
     map.put("key2", taint);

     response.getWriter().println(map.get("key1"));
     response.getWriter().println(map.get("key2"));
     response.getWriter().println(map.get("key3"));

     response.getWriter().println(map);

     Map<String, String> map2 = new HashMap();
     map2.put("key1", "good");
     map2.put(taint, "value");

     response.getWriter().println(map2);
   }
 }