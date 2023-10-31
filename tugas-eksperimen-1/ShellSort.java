import java.util.Arrays;
import java.util.Random;

/*
 * Credits:
 * Code for Randomized Shellsort is entirely taken from the
 * original paper published by Michael T Goodrich.
 * The original title is: Michael T Goodrich. Randomized Shellsort:
 * A Simple Data-Oblivious Sorting Algorithm. Journal of the ACM (JACM), 58(6):1–26, 2011
 * 
 * Source PDF is located in the repository for reference.
 */

public class ShellSort {
    public static final int C=4;
    public static void exchange(int[] a, int i, int j) {
        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
    public static void compareExchange(int[] a, int i, int j) {
        if (((i < j) && (a[i] > a[j])) || ((i > j) && (a[i] < a[j]))) {
            exchange(a, i ,j);
        }
    }

    public static void permuteRandom(int a[], Random rand) {
        for (int i=0; i<a.length; i++ ) {
            exchange(a, i, rand.nextInt(a.length - i) + i); 

        }
    }

    public static void compareRegions(int[] a, int s, int t, int offset, Random rand) {
        int mate[] = new int[offset];
        for (int count=0; count < C; count++) {
            for (int i=0; i < offset; i++) {
                mate[i] = i;
            }
            permuteRandom(mate, rand);
            for (int i=0; i < offset; i++) {
                compareExchange(a, s+i, t+mate[i]);
            }
        }
    }
    
    public static void randomizedShellSort(int[] a) {
        int n = a.length;
        Random rand = new Random();
        for (int offset = n/2; offset > 0; offset /= 2) {
            for (int i = 0; i < n - offset; i += offset) {
                compareRegions(a, i ,i+offset, offset, rand);
            }
            for (int i = n-offset; i >= offset; i -= offset) {
                compareRegions(a, i - offset, i ,offset, rand);
            }
            for (int i = 0; i < n - 3*offset; i += offset) {
                compareRegions(a, i, i+3*offset, offset, rand);
            }
            for (int i = 0; i < n - 2*offset; i += offset) {
                compareRegions(a, i, i+2*offset, offset, rand);
            }
            for (int i = 0; i < n; i += 2*offset) {
                compareRegions(a, i, i+offset, offset, rand);
            }
            for (int i = offset; i < n - offset; i += 2*offset) {
                compareRegions(a, i, i+offset, offset, rand);
            }
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
        randomizedShellSort(arr);
        long endTime = System.nanoTime();
        long endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        System.out.println(description + " took: " + (endTime - startTime) / 1_000_000.0 + " milliseconds and used " + (endMemory - startMemory) + " bytes.");
    }
}