#include<stdio.h>
#include<math.h>
int main() {
    int num;
    scanf("%d", &num);
    int len = num/2 + 1;
    int arr[len];
    int index = 0;
    for (int i = 2; i <= num; i++) {
        while (num % i == 0) {
            arr[index] = i;
            num /= i;
            index++;
        }
    }
    if(num > 1) arr[index++] = num;
    for(int i = 0;i < index ; i++){
        if(i != index - 1){
            printf("%d*",arr[i]);
        }else printf("%d",arr[i]);
    }
    return 0;
}