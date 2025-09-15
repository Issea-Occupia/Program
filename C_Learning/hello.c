#include <stdio.h>
int main(){
    int a;
    scanf("%d",&a);
    printf("%%c:%c,%%d:%d,%%s,%s,%%p,%p",a,a,a,&a);
    return 0;
}