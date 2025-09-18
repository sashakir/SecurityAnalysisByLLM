 package fraunhofer_suite.binarytree;

 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;

 public class TestBasic {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Tree<Integer> tree =
       new Tree<>(1,
                  new Tree<>(2,
                             new Tree<>(3),
                             new Tree<>(4)
                  ),
                  new Tree<>(5)
       );

     if (tree.getLeft().getRight().getValue() == 4) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }

     if (tree.getLeft().getRight() == null) {
       response.getWriter().println(taint);
     }
     else {
       response.getWriter().println(taint);
     }
   }

   class Tree<T> {
     T value;
     Tree<T> left;
     Tree<T> right;

     public Tree(T value, Tree<T> left, Tree<T> right) {
       this.value = value;
       this.left = left;
       this.right = right;
     }

     public Tree(T value) {
       this.value = value;
     }

     public T getValue() {
       return value;
     }

     public Tree<T> getLeft() {
       return left;
     }

     public Tree<T> getRight() {
       return right;
     }
   }
 }