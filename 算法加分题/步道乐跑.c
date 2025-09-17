#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(){
    /*接受跑步人基本信息*/
    int number;
    scanf("%d",&number);
    char ** runners = (char **)malloc(sizeof(char *) * number);//储存跑步人姓名
    int * times = (int *)malloc(sizeof(int) * number);//储存跑步人跑步的次数
    double ** dataset = (double **)malloc(sizeof(double *) * number);//储存每个跑步人的每次里程
    for (size_t i = 0; i < number; i++)
    {
        *(runners + i) = (char *)malloc(sizeof(char) * 21);
        scanf("%s",*(runners + i));
        scanf("%d",times + i);
        *(dataset + i) = (double *)malloc(sizeof(double) * *(times + i));
        /*接受跑步人跑步数据*/
        for (size_t j = 0; j < *(times + i); j++)
        {
            scanf("%lf",(*(dataset + i) +j));
        }
    }
    /*判断总里程*/
    double * odometer = (double *)malloc(sizeof(double) * number);
    char ** total_ = (char **)malloc(sizeof(char *) * number);//记录满足总里程的人
    int odo_qualified = 0; // 记录达标人数
    for (size_t i = 0; i < number; i++)
    {
        double init = 0;
        for (size_t j = 0; j < *(times +i); j++)
        {
            init += *(*(dataset + i) +j);
        }
        if (init >= 120.0)
        {
            *(total_+odo_qualified) = (char *)malloc(sizeof(char) * 21);
            strcpy(*(total_+odo_qualified), *(runners+i));
            odo_qualified++;
        } 
    }
    /*判断3km达标的人*/
    int times_qualified = 0;
    char ** times_ = (char **)malloc(sizeof(char *) * number);//记录3km次数达标人数
    for (size_t i = 0; i < number; i++)
    {
        int finished_times = 0;
        for (size_t j = 0; j < *(times +i); j++)
        {
            if (*(*(dataset + i) +j) >= 3.0)
            {
                finished_times ++;
            }
        }
        if (finished_times >= 40)
        {
            *(times_ + times_qualified) = (char *)malloc(sizeof(char) * 21);
            strcpy(*(times_+times_qualified), *(runners+i));
            times_qualified++;
        }
    }   
}