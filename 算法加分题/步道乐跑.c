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
    /*马上结束啦！就要输出了*/
    char ** fullscore = malloc(sizeof(char *) * (odo_qualified + times_qualified));//满分人名
    int fullcount = 0;//满分人数
    for (size_t i = 0; i < number; i++)
    {
        *(fullscore +i) = (char *)malloc(sizeof(char) * 21);
        strcpy(*(fullscore + fullcount),*(total_ + i));
        fullcount++;
    }
    /*最后的逻辑真的不会写了。就是看从第几项开始，满分数组没有写入，遍历之前的，同时看看times_有没有没有被写进去的，然后附加，得到完整的满分
    然后，再次遍历，得到满分人数，输出。*/    
}
/*用C语言写算法题真是灾难*/