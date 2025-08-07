#include<stdio.h>
enum animal {Dog,Cat,Monkey,Invalid};
void dog(void){
    printf("woof!\n");
}
void cat(void){
    printf("meow!\n");
}
void monkey(void){
    printf("wooo!\n");
}
enum animal select(void)/*这里改成int select(void)也一样*/{
    int num;
    do
    {
        printf("0---dog,1---cat,2---monkey,3---exit : ");
        scanf("%d",&num);
    } while (num <Dog||num >Invalid);
    return num;
    
}
int main(){
    enum animal selected;/*这里改成int selected也一样*/
    do
    {
        switch (selected = select())
        {
        case Dog:dog();break;
        case Cat:cat();break;
        case Monkey:monkey();break;
        }
    } while (selected != Invalid);
    return 0;
    
}
/*事实上，在C语言中，enum类型和int没有本质区别*/