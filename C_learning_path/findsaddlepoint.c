#include<stdio.h>
#define SIZE 5
void FindSaddlePoint(int matrix[SIZE][SIZE]){
    int IsFound = 0;
    for (int i = 0; i < SIZE; i++)/*遍历每行*/
    {
        int PrimaryPoint = matrix[i][0];
        int PrimaryIndex = 0;
        for (int j = 0; j < SIZE; j++)/*找到第i行的最大值*/
        {
            if (PrimaryPoint < matrix[i][j])
            {
                PrimaryIndex = j;
                PrimaryPoint = matrix[i][j];
            }
            
        }
        int IsSaddlePoint = 1;
        for (int k = 0; k < SIZE; k++)/*判断刚刚找到的是不是第PrimaryIndex列中最小的*/
        {
            
            if (PrimaryPoint > matrix[k][PrimaryIndex])/*不是鞍点*/
            {
                IsSaddlePoint = 0;
                break;
            }          
        }
        if (IsSaddlePoint)
            {
                IsFound =1;
                printf("找到鞍点\n[%d][%d]\n值：%d\n",i,PrimaryIndex,PrimaryPoint);
            }  
        
        
    }
    if (!IsFound)
    {
        printf("没有找到鞍点。\n");
    }
    
}
int main() {
    int matrix[SIZE][SIZE] = {
        {1, 5, 6, 8, 5},
        {8, 5, 6, 3, 4},
        {4, 8, 9, 6, 5},
        {5, 8, 9, 3, 7},
        {9, 3, 5, 4, 1}
    };
    
    FindSaddlePoint(matrix);
    return 0;
}