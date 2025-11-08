#include <stdio.h>
#include <math.h>

int main() {
    int left, right;
    scanf("%d%d", &left, &right);
    if (left > right) {  // 保证 left <= right
        int temp = left;
        left = right;
        right = temp;
    }
    int count = 0;   // 已经找到的质数个数
    int num = 2;     // 当前判断的数
    int res = 0;     // 结果和
    while (count < right) {
        int flag = 1;  // 假设 num 是质数
        for (int i = 2; i <= sqrt(num); i++) {
            if (num % i == 0) {
                flag = 0;  // 不是质数
                break;
            }
        }
        if (flag) {  // 是质数
            count++;
            if (count >= left && count <= right)
                res += num;
        }
        num++;
    }
    printf("%d\n", res);
    return 0;
}
