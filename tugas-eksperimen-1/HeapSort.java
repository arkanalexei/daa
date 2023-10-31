import java.util.Arrays;
import java.util.Random;

/*
 * Credits:
 * Code for Max-Heap sort is taken from GeeksForGeeks
 * https://www.geeksforgeeks.org/heap-sort/
 */

public class HeapSort {
    public void sort(int arr[]) {
        int N = arr.length;

        for (int i = N / 2 - 1; i >= 0; i--)
            heapify(arr, N, i);

        for (int i = N - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;

            heapify(arr, i, 0);
        }
    }

    private void heapify(int arr[], int N, int i) {
        int largest = i;
        int l = 2 * i + 1; 
        int r = 2 * i + 2;

        if (l < N && arr[l] > arr[largest])
            largest = l;

        if (r < N && arr[r] > arr[largest])
            largest = r;

        if (largest != i) {
            int swap = arr[i];
            arr[i] = arr[largest];
            arr[largest] = swap;

            heapify(arr, N, largest);
        }
    }

    public static void main(String[] args) {
        // Adjust for small/mid/big size inputs
        int size = (int) Math.pow(2, 16);
        Random rand = new Random();

        int[][] arrays = {
            generateRandomArray(size, rand),
            generateSortedArray(size, rand),
            generateReverseSortedArray(size, rand)
        };

        String[] descriptions = {"Random Input", "Sorted Input", "Reverse Sorted Input"};

        for (int i = 0; i < arrays.length; i++) {
            measureAndPrint(arrays[i], descriptions[i]);
        }
    }

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

    private static void measureAndPrint(int[] arr, String description) {
        long startMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long startTime = System.nanoTime();
        new HeapSort().sort(arr);
        long endTime = System.nanoTime();
        long endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        System.out.println(description + " took: " + (endTime - startTime) / 1_000_000.0 + " milliseconds and used " + (endMemory - startMemory) + " bytes.");
    }
}
