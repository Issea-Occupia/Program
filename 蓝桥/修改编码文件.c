#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  // 请在此输入您的代码
  char c;
  while ((c = getchar()) != EOF)
  {
    if (c >= 97 && c <= 122)
    {
        putchar('L');
    }
    else if (c >= 48 && c<= 57)
    {
        putchar('Q');
    }
    else;
    
  }
  
  return 0;
}