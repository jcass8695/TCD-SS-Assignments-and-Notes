#include <iostream>
#include <iomanip>
#include <ctime>
using namespace std;

int ackermann(int, int);
int ackermannTimed(int, int);

struct riscMetrics {
public:
    int numWindows;
    int windowsUsed;
    int totalOverflows;
    int totalUnderflows;
    int totalCalls;
    int runningOverflows;
    int maxOverflows;
    int registersUsed;
    clock_t start;
    double elapsed;

    void resetMetrics(int _numWindows) {
        numWindows = _numWindows;
        windowsUsed = 0;
        totalOverflows = 0;
        totalUnderflows = 0;
        totalCalls = 0;
        runningOverflows = 0;
        maxOverflows = 0;
        registersUsed = 0;
        elapsed = 0.0;
    }

    void handleOverflow() {
        if(windowsUsed == numWindows) {
            totalOverflows++;
            runningOverflows++;
            if(runningOverflows > maxOverflows) {
                maxOverflows = runningOverflows;
            }
        } else {
            windowsUsed++;
        }
    }

    void handleUnderflow() {
        if(windowsUsed == 2) {
            totalUnderflows++;
            runningOverflows--;
        } else {
            windowsUsed--;
        }
    }

    void resetTimer() {
        start = 0;
        elapsed = 0.0;
    }

    double measureAckermannTime() {
        double mean = 0.0;
        for(int i = 0; i < 10; i++) {
            start = clock();
            ackermannTimed(3, 6);
            elapsed = (double)(clock() - start) / CLOCKS_PER_SEC;
            cout << "Time taken for iteration " << i << ": " << setprecision(6) << elapsed << "s" << endl;
            mean += elapsed;
            resetTimer();
        }

        cout << endl << "Mean time taken: " << mean / 10 << "s" << endl;
    }

    void printResults(int result) {
        cout << "Register Windows: " << numWindows << endl;
        cout << "Result: " << result << endl;
        cout << "Number of calls: " << totalCalls << endl;
        cout << "Total Overflows: " << totalOverflows << endl;
        cout << "Max Overflows: " << maxOverflows << endl;
        cout << "Underflows: " << totalUnderflows << endl;
        cout << "Depth of stack in registers: " << maxOverflows * numWindows << endl << endl;
    }
} riscMetrics;

int ackermann(int x, int y) {
    riscMetrics.totalCalls++;
    riscMetrics.handleOverflow();

    if(x == 0) {
        riscMetrics.handleUnderflow();
        return y + 1;
    } else if(y == 0) {
        int returnVal = ackermann(x-1, 1);
        riscMetrics.handleUnderflow();
        return returnVal;
    } else {
        int returnVal = ackermann(x-1, ackermann(x, y - 1));
        riscMetrics.handleUnderflow();
        return returnVal;
    }
}

int ackermannTimed(int x, int y) {
    if(x == 0) {
        return y + 1;
    } else if(y == 0) {
        return ackermannTimed(x-1, 1);
    } else {
        return ackermannTimed(x-1, ackermannTimed(x, y - 1));
    }
}

int main() {
    int test1 = 6;
    int test2 = 8;
    int test3 = 16;

    riscMetrics.resetMetrics(test1);
    int result = ackermann(3, 6);
    riscMetrics.printResults(result);

    riscMetrics.resetMetrics(test2);
    result = ackermann(3, 6);
    riscMetrics.printResults(result);

    riscMetrics.resetMetrics(test3);
    result = ackermann(3, 6);
    riscMetrics.printResults(result);

    riscMetrics.measureAckermannTime();

    return 0;
}
