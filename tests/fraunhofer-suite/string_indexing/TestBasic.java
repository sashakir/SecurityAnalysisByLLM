 package fraunhofer_suite.string_indexing;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestBasic {
   public static void test(HttpServletRequest request, HttpServletResponse response) throws IOException {

     String taint = request.getHeader("value");

     String guess = "ABC";
     char switchTarget = guess.charAt(1);

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