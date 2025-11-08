#include<stdio.h>
#include<stdlib.h>
bool isPalindrome(int x) {
   if (x < 0 ) return false;
   if(x >= 0 && x < 10 ) return true;
   int count = 0;
   int x1 = x;
   while (x1 > 0)
   {
        x1 /= 10;
        count++;
   }
   int * nums = malloc(sizeof(int) * count);
   for (size_t i = 0; i < count; i++)
   {
    nums[i] = x % 10;
    x /= 10;
   }
   int a = 0;
   int b = count -1;
   while (a<b)
   {
        if (nums[a] != nums[b]) return false;
        a++;
        b--;
   }
   return true;
}