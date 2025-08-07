#include <stdio.h>
#include <string.h>
#include <ctype.h>
int main(){
    char original_password[] = "eg][l^sdm(i)YfWqq\\-u";
    int len = strlen(original_password);
    for (int shift = -50; shift < 50; shift++)
    {
        printf("shift%d\n",shift);
        for (int i = 0; i < len; i++)
        {
            char pre_processed = original_password[i];
            char result = pre_processed + shift;
            if (isprint(result))
            {
                putchar(result);
            }
            else{
                putchar('.');
            }           
        }
        printf("\n");     
    }
    
}