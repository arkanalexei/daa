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


public class ShellSort implements SortingAlgorithm {
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
    
    @Override
    public void sort(int[] a) {
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
}