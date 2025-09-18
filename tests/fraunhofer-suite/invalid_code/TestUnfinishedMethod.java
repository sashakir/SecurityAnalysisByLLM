 package fraunhofer_suite.invalid_code;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.net.URL;

 public class TestUnfinishedMethod {
   public URL getMissingNixonTapes() {

   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     response.getWriter().println(taint);
   }
 }