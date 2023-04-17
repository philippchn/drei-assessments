package com.company;

import java.io.*;
import java.net.*;
import java.util.concurrent.TimeUnit;

public class Main {
    public static int extractData(String measurement){
        return Integer.parseInt(measurement.substring(measurement.lastIndexOf(":")+1, measurement.lastIndexOf("}")));
    }
    public static int getAnswer(){
        String response = "";
        try {
            URL url = new URL("http://127.0.0.1:7744/datameasure/data1");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            response = in.readLine();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return extractData(response);
    }
    public static void main(String[] args) throws InterruptedException {
        int timeOut = 10; // HOW LONG THE PROGRAMM SHOULD WAIT BETWEEN EVERY CALL
        System.out.println("Programm Start. Checking every " + timeOut + " seconds!");
        double SUM_GAUGE = 0;
        int COUNT_GAUGE = 0;
        double longTimeAverage = 0;
        double counter = getAnswer();
        TimeUnit.SECONDS.sleep(timeOut);
        double bottlesPerSecond;
        while(true) {
            System.out.println("Current count: " + counter);
            int newCount = getAnswer();
            System.out.println("New count: " + newCount);
            double difference = newCount - counter;
            if (newCount < counter || Math.abs(difference) > 200) {
                System.out.println("Programm restart");
                System.out.println("------------------");
                TimeUnit.SECONDS.sleep(timeOut);
                counter = getAnswer();
                continue;
            }
            bottlesPerSecond = difference / timeOut;
            counter = counter + difference;
            System.out.println("Current B/S: " + bottlesPerSecond);
            System.out.println("Average B/S during " + (COUNT_GAUGE * timeOut) + " seconds: " + longTimeAverage);
            if(longTimeAverage != 0 && ((longTimeAverage * 0.9) - bottlesPerSecond > 0 || bottlesPerSecond - (longTimeAverage * 1.1)  > 0)){
                System.out.println("The B/S is 10% away from average B/S. Value might be wrong");
                System.out.println("Long time Average won't be updated with those values");
            }else{
                SUM_GAUGE = SUM_GAUGE + bottlesPerSecond;
                COUNT_GAUGE = COUNT_GAUGE + 1;
                longTimeAverage = (SUM_GAUGE / COUNT_GAUGE);
            }
            System.out.println("------------------");
            TimeUnit.SECONDS.sleep(timeOut);
        }
    }
}
