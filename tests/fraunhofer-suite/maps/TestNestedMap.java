 package fraunhofer_suite.maps;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.HashMap;
 import java.util.Map;

 public class TestNestedMap {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Map<String, Map<String, String>> map = new HashMap<>();
     map.put("key1a", new HashMap<>());
     map.put("key2a", new HashMap<>());
     map.get("key1a").put("key1b", "value");
     map.get("key1a").put("key2b", taint);
     map.get("key2a").put("key1b", taint);
     map.get("key2a").put("key2b", "value");

     response.getWriter().println(map.get("key1a").get("key1b"));
     response.getWriter().println(map.get("key1a").get("key2b"));
     response.getWriter().println(map.get("key2a").get("key1b"));
     response.getWriter().println(map.get("key2a").get("key2b"));
     response.getWriter().println(map.get("key2a").get("key2c"));
   }
 }