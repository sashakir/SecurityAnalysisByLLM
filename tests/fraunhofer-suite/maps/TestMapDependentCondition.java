 package fraunhofer_suite.maps;


 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 import java.io.IOException;
 import java.util.HashMap;
 import java.util.Map;

 public class TestMapDependentCondition {
   public void test(HttpServletRequest request, HttpServletResponse response) throws IOException {
     String taint = request.getHeader("value");
     Map<String, Integer> prices = new HashMap<>();
     updateCarPrice(new Car("Audi"), prices);
     updateCarPrice(new Car("Mercedes"), prices);

     if (prices.get("Audi") < 70_000)
       response.getWriter().println(taint);
     else
       response.getWriter().println(taint);

     if (prices.get("BMW") != null)
       response.getWriter().println(taint);
     else
       response.getWriter().println(taint);

     if (prices.get("Mercedes") != null)
       response.getWriter().println(taint);
     else
       response.getWriter().println(taint);
   }

   class Car {
     String modelId;

     public Car(String modelId) {
       this.modelId = modelId;
     }
   }

   int getAudiPrice() { return 65_000; }
   int getMercedesPrice() { return 75_000; }

   void updateCarPrice(Car car, Map<String, Integer> prices) {
     if (car.modelId.equals("Audi"))
       prices.put(car.modelId, getAudiPrice());
     else
       prices.put(car.modelId, getMercedesPrice());
   }
 }