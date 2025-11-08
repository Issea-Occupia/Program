#include <stdio.h>
int main(){
    int m,n;
    scanf("%d%d",&m,&n);
    int arr[m][n];
    for (size_t i = 0; i < m; i++)
    {
        for (size_t j = 0; j < n; j++)
        {
            scanf("%d",&arr[i][j]);
        }
    }
    for (size_t i = 0; i < m; i++)
    {
        int left = -1;
        int right = -1;
        int current_left = -1;
        int current_right = -1;
        for (size_t j = 0; j < n; j++)
        {
            if(arr[i][j] == 1){
                if(current_left == -1){
                    current_left = current_right = j;
                }else {
                    current_right = j;
                }
                if(left == -1 || current_right - current_left > right -left){
                    right = current_right;
                    left = current_left;
                    }
            }
            if(arr[i][j] == 0){
                current_left = current_right =-1;
            }
        }
        printf("%d %d\n",left,right);
    }
    return 0;
}