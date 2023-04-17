package net.inemar.datameasure;

import java.util.Random;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.atomic.AtomicInteger;

import com.sun.net.httpserver.*;



class Resp {
    static   void sendResponse200(HttpExchange httpExchange,String data) throws IOException {

        httpExchange.sendResponseHeaders(200,0);
        OutputStream outputStream = httpExchange.getResponseBody();
                
                outputStream.write(data.getBytes());
                outputStream.flush();
                outputStream.close();
        
    
    
    }

    static   void sendError(HttpExchange httpExchange,int error,String data) throws IOException {

        httpExchange.sendResponseHeaders(error,0);
        OutputStream outputStream = httpExchange.getResponseBody();
                
                outputStream.write(data.getBytes());
                outputStream.flush();
                outputStream.close();
        
    
    
    }

    
    static Random random=new Random(System.currentTimeMillis());


 
}

final class MyHelloHandler implements HttpHandler {    
    @Override    
    public void handle(HttpExchange httpExchange) throws IOException {
       System.out.println("Got "+httpExchange.getRequestMethod()); 
      String method=httpExchange.getRequestMethod();
      if("GET".equals(method)) { 
         Resp.sendResponse200(httpExchange, "Hello this is the datameasure simulator !");
       }else  { 
           Resp.sendError(httpExchange, 400, "Only GET Method is allowed- Got: "+method);
        }  
    }
  }

  final class GetDataHandler implements HttpHandler {    
    @Override    
    public void handle(HttpExchange httpExchange) throws IOException {
      String method=httpExchange.getRequestMethod();
      //String query=httpExchange.getRequestURI().getQuery();
      if("GET".equals(method)) { 
        String result="{\"measurepoint\": \"Point Blanc\",\"data\":"+App.measure_value.get()+"}";
        Resp.sendResponse200(httpExchange,result);
       }else  { 
           Resp.sendError(httpExchange, 400, "Only GET Method is allowed- Got: "+method);
        }  
    }
  }

public class App {

    static AtomicInteger measure_value=new AtomicInteger(0);


    public static void main( String[] args ) throws IOException 

    {
        System.out.println("Version 1.2");
        HttpServer server = HttpServer.create(new InetSocketAddress("localhost", 7744), 0);


        ThreadPoolExecutor threadPoolExecutor = (ThreadPoolExecutor)Executors.newFixedThreadPool(10);
        server.createContext("/hello", new  MyHelloHandler());
        server.createContext("/datameasure/data1", new  GetDataHandler());
        server.setExecutor(threadPoolExecutor);
        server.start();

        System.out.println(" Server started on port 7744");

        //simulate values

        int speed = 30;
        int target=speed;
        Random random=new Random(System.currentTimeMillis());
        int value=0;
        int outage=0;
        int change_speed=3;
        while(true) {


            //change target
            //System.out.println(random.nextInt(50));
            if ((random.nextInt(100))<10) {
                target=20+random.nextInt(20);
                System.out.println("New target "+target);
            }

            //change speed
            change_speed=change_speed-1;

            if (change_speed<=0) {
               if (speed<target) {
                    speed=speed+1;
                    System.out.println("New speed "+speed +"( "+target+")");
                };
                if (speed>target) {
                    speed=speed-1 ;
                    System.out.println("New speed "+speed +"( "+target+")");
                };
                change_speed=3;
            };

        
            if (speed<20) {
                speed=20;
            };
            if (speed>40) {
                speed=40;
            }


            value=value+speed;
            value=value%1024;

            //reset
            if ((random.nextInt(1000))<5) {
                System.out.println("Reset");
                value=0;
            }


            //outage
            if ((random.nextInt(100))<3) {
                outage=(random.nextInt(4))*4+5;
                System.out.println("Outage "+outage);
            }

            if (outage<=0) {
                measure_value.set(value);
                outage=0;
            } else {
                outage=outage-1;
            }

            System.out.println("Value "+measure_value+"  Bottles/sec: "+(speed/2.0));
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                ;
            }

        }

        
    }
}
