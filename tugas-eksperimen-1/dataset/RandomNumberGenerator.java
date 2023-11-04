package dataset;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class RandomNumberGenerator {
    public static void main(String[] args) {
        int n = (int) Math.pow(2,16);
        String fileName = "big-random.txt";
        
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
            Random rand = new Random();
            
            for (int i = 0; i < n; i++) {
                int number = rand.nextInt(n);
                writer.write(Integer.toString(number));
                writer.newLine();
            }
            
            writer.close();
            System.out.println("Random numbers written to " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}