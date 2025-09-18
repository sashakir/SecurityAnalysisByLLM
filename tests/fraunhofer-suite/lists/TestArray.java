 package fraunhofer_suite.lists;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.ArrayList;
 import java.util.List;

 public class TestArray {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     List<String> valuesList = new ArrayList<String>();
     valuesList.add("safe");
     valuesList.add(taint);
     valuesList.add("moresafe");

     response.getWriter().println(valuesList.get(0));
     response.getWriter().println(valuesList.get(1));
     response.getWriter().println(valuesList.get(2));

     valuesList.remove(0);

     response.getWriter().println(valuesList.get(0));
     response.getWriter().println(valuesList.get(1));
   }
 }