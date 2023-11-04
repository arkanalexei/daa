package dataset;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

public class ReverseSortedNumberGenerator {
    public static void main(String[] args) {
        int n = (int) Math.pow(2,16);
        String fileName = "big-reverse.txt";

        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
            Random rand = new Random();

            int[] numbers = new int[n];
            for (int i = 0; i < n; i++) {
                numbers[i] = rand.nextInt(n);
            }

            Arrays.sort(numbers);
            for (int i = 0; i < n / 2; i++) {
                int temp = numbers[i];
                numbers[i] = numbers[n - i - 1];
                numbers[n - i - 1] = temp;
            }

            for (int number : numbers) {
                writer.write(Integer.toString(number));
                writer.newLine();
            }

            writer.close();
            System.out.println("Reverse sorted random numbers written to " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
