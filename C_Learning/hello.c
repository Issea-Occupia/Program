#include <stdio.h>
void change(int* a);
int main(){
    int* a;
    a = 6;
    printf("%d",*a);
    void change(int* a);
    printf("%d",*a);
    return 0;
}
void change(int* a){
    *a = 10;
}