/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
#include<stdlib.h>
#include<stdio.h>
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    int* res = (int *)malloc(sizeof(int) * 2);
    int a = 0;
    int b = numsSize - 1;
    while (a < b)
    {
        int answer = nums[a] +nums[b];
        if (answer == target)
        {
            res[0] = a;
            res[1] = b;
            break;
        }else if (answer > target)
        {
            b--;
        }else{a++;}
    }
    *returnSize = 2;
    return res;
}
int main(){
    int nums[] = {2,7,11,15};
    int b[] = {0,0};
    int* a = twoSum(nums,4,9,b);
    printf("%d%d",a[0],a[1]);
    return 0;
}