#include <stdio.h>
int main(){
   int input;
   scanf("%d",&input);
   int __100 = input / 100;
   input -= __100 * 100;
   int ___50 = input / 50;
   input -= ___50 * 50;
   int ___20 = input / 20;
   input -= ___20 * 20;
   int ___10 = input / 10;
   input -= ___10 * 10;
   int ____5 = input / 5;
   input -= ____5 * 5;
   int ____1 = input;
   printf("%d,%d,%d,%d,%d,%d",__100,___50,___20,___10,____5,____1);
   return 0;
}