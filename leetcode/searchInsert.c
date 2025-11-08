#include<stdio.h>
int searchInsert(int* nums, int numsSize, int target) {
    if (numsSize == 1) {
        return (target <= nums[0]) ? 0 : 1;
    }
    if (target <= nums[0]) return 0; 
    if (target > nums[numsSize - 1]) return numsSize;

    for (int i = 0; i < numsSize - 1; i++) {
        int a = nums[i];
        int b = nums[i + 1];

        if (target == a) return i;
        if (target == b) return i + 1;
        if (target > a && target < b) return i + 1;
    }

    return numsSize;
}
int main(){
    int nums[] = {1};
    int b = searchInsert(nums, 1, 0);

    printf("%d",b);
    return 0;
}
