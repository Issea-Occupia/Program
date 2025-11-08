#include<stdio.h>
#include<math.h>
int prime(int);
int main(){
    int i;
    scanf("%d",&i);
    int res = prime(i);
    switch (res)
    {
    case 0:
        printf("yes");
        break;
    default:
    printf("no");
        break;
    }
    return 0;
}
int prime(int n){
    for(int i = 2 ; i <= sqrt(n)+1 ; i++) if(n % i==  0) return 0;
    return 1;
}