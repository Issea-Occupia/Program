typedef struct {
    int value;
    int index;
} Pair;
int findLucky(int* arr, int arrSize) {
    Pair nums[arrSize];
    int j = 0;
    int res = -1;
    int count = 0;
    for (int i = 0;i < arrSize - 1;i++){
        if(arr[i] == arr[i+1]) count ++;
        if(arr[i] < arr[i+1]){
            nums[j].value = arr[i];
            nums[j].index = count + 1;
            count = 0;
            j++;
        }
    }
    for (int i = 0;i < arrSize;i++){
        res = (nums[j].value == nums[j].index)?(nums[j].value):(-1);
    }
}