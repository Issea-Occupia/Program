#include <stdio.h>
#include <stdlib.h>
int main(){
    /*接受跑步人基本信息*/
    int number;
    scanf("%d",&number);
    char ** runners = (char **)malloc(sizeof(char *) * number);
    int * times = (int *)malloc(sizeof(int) * number);
    for (size_t i = 0; i < number; i++)
    {
        *(runners + i) = (char *)malloc(sizeof(char) * 101);
        scanf("%s",*(runners + i));
        scanf("%d",times + i);
        int * detailed_data = (int)malloc(sizeof(int) * *(times + i));
        /*接受跑步人跑步数据*/
        for (size_t j = 0; i < *(times + i); j++)
        {
            scanf("%d",detailed_data + j);
        }
    }
    /*判断总里程*/
    
}