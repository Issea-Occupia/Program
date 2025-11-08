#include <stdio.h>
int main(){

}
void odd_even(int* src,int count){
    for (size_t i = 0; i < count; i++)
    {
        for (size_t j = i%2; j < count-1; j+=2)
        {
            if (src[j] > src[j+1])
            {
                int temp = src[j];
                src[j] = src[j+1];
                src[j+1] = temp;
            }
        }
    }
}