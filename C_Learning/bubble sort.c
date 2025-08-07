#include<stdio.h>
void bubble_sorting(int array[],int arrayelments){
    int n = arrayelments;
    for (int i = 0; i < n-1; i++)
    {
        int issorted = 0;
        for (int j = 0; j < n-1-i; j++)
        {
            if (array[j] > array[j+1])
            {
                int temp = array[j+1];
                array[j+1] = array[j];
                array[j] = temp; 
                issorted = 1;
            }
        }
        if (!issorted)
        {
            break;
        }
    }
}
int main(){
    int num[] = {1,1,4,5,1,4,1,9,1,9,8,1,0};
    int elements = sizeof(num)/sizeof(num[0]);
    bubble_sorting(num,elements);
    for (int i = 0; i < elements; i++)
    {
        printf("%d",num[i]);
    }
}