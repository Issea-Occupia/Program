#include <stdio.h>
#define ROWS 3
#define COLS 3

void findSaddlePoint(int matrix[ROWS][COLS]) {
    for (int i = 0; i < ROWS; i++) {
        // 1. 找到当前行的最大值
        int rowMax = matrix[i][0];
        int colIndex = 0;
        
        for (int j = 1; j < COLS; j++) {
            if (matrix[i][j] > rowMax) {
                rowMax = matrix[i][j];
                colIndex = j;
            }
        }
        
        // 2. 检查这个值是否是所在列的最小值
        int isSaddlePoint = 1;
        for (int k = 0; k < ROWS; k++) {
            if (matrix[k][colIndex] < rowMax) {
                isSaddlePoint = 0;
                break;
            }
        }
        
        // 3. 如果是鞍点，打印并返回
        if (isSaddlePoint) {
            printf("鞍点: [%d][%d] = %d\n", i, colIndex, rowMax);
            return;
        }
    }
    
    printf("矩阵中没有鞍点\n");
}

int main() {
    int matrix1[ROWS][COLS] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    int matrix2[ROWS][COLS] = {
        {9, 8, 7},
        {5, 3, 2},
        {6, 4, 1}
    };
    
    printf("矩阵1:\n");
    findSaddlePoint(matrix1);
    
    printf("\n矩阵2:\n");
    findSaddlePoint(matrix2);
    
    return 0;
}