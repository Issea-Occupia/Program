#include <stdio.h>
int f(int steps){
    switch (steps)
    {
    case 0:
        return 1;
    case 1:
        return 1;
    case 2:
        return 2;
    }
    return f(steps -1) + f(steps - 2);
}
int main(){
    int steps;
    do
    {
        printf("Here is a man climbs the stair,type the number of steps: ");
        scanf("%d",&steps);
    } while (steps < 0);
    printf("He has %d methods to climb.",f(steps));
}
/*落后的版本，算到50就完全卡死了，可能因为多次递归调用（反向斐波那契）*/