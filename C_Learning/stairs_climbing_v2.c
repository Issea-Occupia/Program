#include <stdio.h>
int f(int);
int main(){
    int steps;
    do
    {
        printf("Here is a man climbs the stair,type the number of steps: ");
        scanf("%d",&steps);
    } while (steps < 0);
    printf("He has %d methods to climb.",f(steps));
}
int f(int steps){
    int a =1;
    int b =1;
    int c =1;
    int frequency =1;
    while (frequency < steps)
    {
        c = a + b;
        int temp_a = b;
        a = temp_a;
        b = c;
        frequency++;
    }
    return c; 
}
