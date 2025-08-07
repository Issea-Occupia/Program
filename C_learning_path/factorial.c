#include <stdio.h>
int factorial(int num){
    int result =1;
    if (num > 0)
    {
        for (int i = num; i > 0; i--)
        {
            result *= num;
            num--;
        }
        return result;        
    }
    else
    printf("invalid input!");
    return 0;
}
int main(){
    int num,result;
    printf("let my help you to calculat the factorial!type an integrate number:");
    scanf("%d",&num);
    result = factorial(num);
    if (result)
    {
        printf("here is the result:%d",result);
    }
    return 0;
    
}