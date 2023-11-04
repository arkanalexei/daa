import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;

interface SortingAlgorithm {
    void sort(int[] arr);
}

public class Test {
    private static int[] readArrayFromFile(String filePath) {
        List<Integer> numbers = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                numbers.add(Integer.parseInt(line.trim()));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return numbers.stream().mapToInt(i -> i).toArray();
    }

    private static long getMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }

    private static void printHeader() {
        System.out.printf("| %-15s | %-15s | %-10s | %-10s | %-10s |%n", 
                          "Size", "Data Type", "Algorithm", "Time (ms)", "Memory (B)");
        System.out.println("|-----------------|-----------------|------------|------------|------------|");
    }

    private static void printStatistics(String size, String algorithm, String description, double timeInMs, long memoryInBytes) {
        System.out.printf("| %-15s | %-15s | %-10s | %-10.2f | %-10d |%n", 
                          size, description, algorithm, timeInMs, memoryInBytes);
    }

    private static void measureAndPrint(String size, SortingAlgorithm algorithm, int[] arr, String description) {
        int runs = 10;
        double totalTimeInMs = 0;
        long totalMemoryInBytes = 0;

        for (int i = 0; i < runs; i++) {
            int[] copyArr = Arrays.copyOf(arr, arr.length);

            long startTime = System.nanoTime();
            System.gc();
            long startMemory = getMemoryUsage();

            algorithm.sort(copyArr);

            long endMemory = getMemoryUsage();
            long endTime = System.nanoTime();

            totalTimeInMs += (endTime - startTime) / 1_000_000;
            totalMemoryInBytes += endMemory - startMemory;
        }

        double avgTimeInMs = totalTimeInMs / runs;
        long avgMemoryInBytes = totalMemoryInBytes / runs;

        printStatistics(size, algorithm.getClass().getSimpleName(), description, avgTimeInMs, avgMemoryInBytes);
    }

    public static void main(String[] args) {
        String[] sizes = {"small", "medium", "big"};
        String[] types = {"sorted", "random", "reverse"};
        ShellSort shellSort = new ShellSort();
        HeapSort heapSort = new HeapSort();

        String outputFilePath = "output.txt";

        try (PrintStream fileOut = new PrintStream(new FileOutputStream(outputFilePath))) {
            System.setOut(fileOut);

            printHeader();

            for (String size : sizes) {
                for (String type : types) {
                    String filePath = "tugas-eksperimen-1/dataset/" + size + "-" + type + ".txt";
                    int[] array = readArrayFromFile(filePath);

                    measureAndPrint(size, shellSort, array, type);
                    measureAndPrint(size, heapSort, array, type);
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
