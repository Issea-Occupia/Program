#include<stdio.h>
int main(){
    double num[10];
    for (size_t i = 0; i < 20; i++)
    {
        printf("%d\n",*(num + i));
    }
    return 0;
}