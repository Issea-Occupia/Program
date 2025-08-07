#include <stdio.h>
int combination(int i,int j){
    if (i>j||i<0||j<0)
    {
        return -1;
    }
    if (i == j||i == 0)
    {
        return 1;
    }
    if (i == 1)
    {
        return j;
    }
    return combination(i-1,j-1)+combination(i,j-1);
}
int main(){
    int a,b,result;
    printf("求组合数Cab！输入两个数");
    printf("a:");
    scanf("%d",&a);
    printf("b:");
    scanf("%d",&b);
    result = combination(b,a);
    if (result == -1)
    {
        printf("invalid input!!!");
    }
    else{
        printf("%d",result);
    }
}
/*在这个程序中，cab是说，大c下面是a，上面是b*/