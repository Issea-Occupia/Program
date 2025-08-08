#include <stdio.h>
#include <string.h>
#include <ctype.h>
int main(){
    char str_1[100];
    char str_2[100];
    printf("Please Type The Encrypting Alphabet:");
    scanf("%s",str_1);
    printf("Please Type The Password:");
    scanf("%s",str_2);
    int len_1 = strlen(str_2);
    for (int i = 0; i < len_1; i++)
    {
        char c = tolower(str_2[i]) - 'a';
        char k = tolower(str_1[i%strlen(str_1)]) - 'a';
        char result = (c-k +26)%26 + 'a';
        putchar(result);
    }
    return 0;
}