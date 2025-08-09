#include <stdio.h>
void to_binary(int);
int main(){
    printf("type a integer and i will convert it into binary!");
    int num;
    scanf("%d",&num);
    to_binary(num);
    return 0;
}
void to_binary(int num){
    int r = num%2;
    if (num >= 2){
        to_binary(num / 2);
    }
    putchar(r == 0?'0':'1');
}
