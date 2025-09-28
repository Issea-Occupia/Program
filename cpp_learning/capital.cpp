#include <cstdio>
int main(){
    char ch;
    while ((ch = getchar()) != '\n')
    {
        char ch2 = ch + 32;
        putchar(ch2);
    }
    return 0;
}