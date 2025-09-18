 package fraunhofer_suite.string_indexing;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestUnknownString {
   public static void test(HttpServletRequest request, HttpServletResponse response, String letters) throws IOException {

     String taint = request.getHeader("value");

     char switchTarget = letters.charAt(1);

     switch (switchTarget) {
       case 'A':
         response.getWriter().println(taint);
         break;
       case 'B':
         response.getWriter().println(taint);
         break;
       case 'C':
       case 'D':
         response.getWriter().println(taint);
         break;
       default:
         break;
     }
   }
 }