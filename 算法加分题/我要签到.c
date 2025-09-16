#include <stdio.h>
#include <stdlib.h>
int CompareFunction(const void * a,const void * b){
     return ( *(int*)a - *(int*)b );
}
int main(){
    /*先接受签到人数和监控记录数*/
    int checked,recorded;
    scanf("%d %d",&checked,&recorded);
    int *checker = (int *)malloc(sizeof(int) * checked);
    int *recorder = (int *)malloc(sizeof(int) * recorded);
    /*接受签到人的学号*/
    for (size_t i = 0; i < checked; i++)
    {
        int temp1;
        scanf("%d",&temp1);
        *(checker + i) = temp1;
    }
    /*接受监控记录的学号*/
    for (size_t i = 0; i < recorded; i++)
    {
        int temp1;
        scanf("%d",&temp1);
        *(recorder + i) = temp1;
    }
    /*处理监控记录的学号*/
    qsort(recorder,recorded,sizeof(int),CompareFunction);
    /*双指针判别相同人*/
    int temp2 = 0;
    for (size_t i = 0; i < recorded-1; i++)
    {
        if (*(recorder + i) == *(recorder + i +1)) temp2++,i++,printf("%d\n",*(recorder + i));
    }
    free(checker,recorder);
}