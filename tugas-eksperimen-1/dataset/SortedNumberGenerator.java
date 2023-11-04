package dataset;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

public class SortedNumberGenerator {
    public static void main(String[] args) {
        int n = (int) Math.pow(2,16);
        String fileName = "big-sorted.txt";

        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
            Random rand = new Random();

            int[] numbers = new int[n];
            for (int i = 0; i < n; i++) {
                numbers[i] = rand.nextInt(n);
            }

            Arrays.sort(numbers);

            for (int number : numbers) {
                writer.write(Integer.toString(number));
                writer.newLine();
            }

            writer.close();
            System.out.println("Sorted random numbers written to " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
