#include <stdio.h>

int main() {
    int num = 5;
    int i;
    long long factorial = 1;
    if (num < 0) {
        printf("Factorial is not defined for negative numbers.\n");
    } else {
        for (i = 1; i <= num; i++) {
            factorial *= i;
        }
        printf("Factorial of %d is %lld\n", num, factorial);
    }

    return 0;
}
