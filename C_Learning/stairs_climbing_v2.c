#include <stdio.h>
long long f(int);
int main(){
    int steps;
    do
    {
        printf("Here is a man climbs the stair,type the number of steps(positive interge): ");
        scanf("%d",&steps);
    } while (steps < 0);
    printf("He has %lld methods to climb.",f(steps));
}
long long f(int steps){
    long long a =1;/*使用int溢出成了负数......*/
    long long b =1;
    long long c =1;
    if (steps <= 2)
    {
        return steps;
    }
    else{
        for (int i = 1; i < steps; i++)
        {
            c = a + b;
            a = b;
            b = c;
        }
    }
    return c; 
}
/*f代表函数，表示了楼梯数目与攀爬方式的映射关系(正向斐波那契)*/