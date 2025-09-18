 package fraunhofer_suite.lists;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestLinkedList {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     MyList l = new MyList("1", new MyList("2", new MyList(taint, null)));

     response.getWriter().println(l.getValue());
     response.getWriter().println(l.getNext().getValue());
     response.getWriter().println(l.getNext().getNext().getValue());

     if (l.getNext().getNext() == null)
       response.getWriter().println(taint);
     else
       response.getWriter().println(taint);

     if (l.getNext().getNext().getNext() == null)
       response.getWriter().println(taint);
     else
       response.getWriter().println(taint);

     if (l.getNext().getValue().equals("2"))
       response.getWriter().println(taint);
     else
       response.getWriter().println(taint);
   }
 }

 class MyList {
   String val;
   MyList next;

   MyList(String v, MyList n) {
     val = v;
     next = n;
   }

   MyList getNext() {
     return next;
   }

   String getValue() {
     return val;
   }
 }