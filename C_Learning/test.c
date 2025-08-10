#include<stdio.h>
void min_of(const int v[],int n ){
    int min=v[0];
    if (n <= 0)
    {
        printf("Error array");
        return;
    }
    for (int i = 1; i < n; i++)
    {
        if (v[i] <= 0)
        {
            printf("you cannot use this negative array!");
            printf("negative number is in this array");
            return;
        }
        else{
            if (v[i] < min)
            {
                min = v[i];
            }    
        }      
    }
    printf("the min number is %d",min);    
}
int main(){
    int v[] = {9,5,11,7,2};
    min_of(v,5);
    return 0;
}