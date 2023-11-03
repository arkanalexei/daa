import java.util.Arrays;
import java.util.Random;

interface SortingAlgorithm {
    void sort(int[] arr);
}

public class Test {
    private static int[] generateRandomArray(int size, Random rand) {
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = rand.nextInt(10000);
        }
        return arr;
    }

    private static int[] generateSortedArray(int size, Random rand) {
        int[] arr = generateRandomArray(size, rand);
        Arrays.sort(arr);
        return arr;
    }

    private static int[] generateReverseSortedArray(int size, Random rand) {
        int[] arr = generateSortedArray(size, rand);
        for (int i = 0, j = size - 1; i < j; i++, j--) {
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
        return arr;
    }

    private static long getMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        System.gc();
        return runtime.totalMemory() - runtime.freeMemory();
    }

    private static void printStatistics(String algorithm, String description, double timeInMs, long memoryInBytes) {
        System.out.println("Algorithm: "+ algorithm);
        System.out.println("Data: " + description);
        System.out.println("Time: " + timeInMs + " ms");
        System.out.println("Memory: " + memoryInBytes + " B");
        System.out.println();
    }

    private static void measureAndPrint(SortingAlgorithm algorithm, int[] arr, String description) {        
        long startTime = System.nanoTime();
        long startMemory = getMemoryUsage();

        algorithm.sort(arr);

        long endTime = System.nanoTime();
        long endMemory = getMemoryUsage();

        double timeInMs = (endTime - startTime) / 1_000_000.0;
        long memoryInBytes = endMemory - startMemory;

        printStatistics(algorithm.getClass().getSimpleName(), description, timeInMs, memoryInBytes);
    }

    public static void main(String[] args) {
        int size = (int) Math.pow(2, 16);
        Random rand = new Random();
        ShellSort shellSort = new ShellSort();
        HeapSort heapSort = new HeapSort();

        int[][] arrays = {
            generateSortedArray(size, rand),
            generateRandomArray(size, rand),
            generateReverseSortedArray(size, rand)
        };

        String[] descriptions = {"Sorted Input", "Random Input", "Reverse Sorted Input"};

        for (int i = 0; i < arrays.length; i++) {
            measureAndPrint(shellSort, arrays[i], descriptions[i]);
        }

        System.out.println("Testing HeapSort:");
        for (int i = 0; i < arrays.length; i++) {
            measureAndPrint(heapSort, arrays[i], descriptions[i]);
        }
    }
}
