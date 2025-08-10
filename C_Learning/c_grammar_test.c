#include <stdio.h>
#define count 3
int main(){
    int content = 0;
    int num[3][3][3][3];
    for (size_t i = 0; i < 3; i++)
    {
        for (size_t j = 0; j < 3; j++)
        {
            for (size_t k = 0; k < count; k++)
            {
                for (size_t l = 0; l < count; l++)
                {
                    num[i][j][k][l] = content;
                    content++;
                }   
            }            
        }        
    }
    for (size_t i = 0; i < count; i++)
    {
        for (size_t j = 0; j < count; j++)
        {
            for (size_t k = 0; k < count; k++)
            {
                for (size_t l = 0; l < count; l++)
                {
                    printf("%d ",num[i][j][k][l]);
                }                
            }            
        }        
    }
    printf("****num: %d\n", ****num);
    printf("***(*num+1): %d\n", ***(*num+1));
    printf("**(**num+1): %d\n", **(**num+1));
    printf("***(*(num+1)): %d\n", ***(*(num+1)));
    printf("**(*(*num+1)+1): %d\n", **(*(*num+1)+1));
    printf("*(*(*num+1)+1)+1: %d\n", *(*(*num+1)+1)+1);
    printf("(*(*(*num+1)+1)+1)[0]: %d\n", (*(*(*num+1)+1)+1)[0]);   
}