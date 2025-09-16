#include <stdio.h>
#include <stdlib.h>
int main(){
    /*接受跑步人基本信息*/
    int number;
    scanf("%d",&number);
    char ** runners = (char **)malloc(sizeof(char *) * number);
    int * times = (int *)malloc(sizeof(int) * number);
    int ** dataset = (int **)malloc(sizeof(int *) * number);
    for (size_t i = 0; i < number; i++)
    {
        *(runners + i) = (char *)malloc(sizeof(char) * 21);
        scanf("%s",*(runners + i));
        scanf("%d",times + i);
        *(dataset + i) = (int *)malloc(sizeof(int) * *(times + i));
        /*接受跑步人跑步数据*/
        for (size_t j = 0; j < *(times + i); j++)
        {
            scanf("%d",(*(dataset + i) +j));
        }
    }
    /*判断总里程*/
    int * odometer = (int*)malloc(sizeof(int) * number);
    for (size_t i = 0; i < number; i++)
    {
        for (size_t j = 0; j < *(times +i); i++)
        {
            
        }
        
    }
    
}