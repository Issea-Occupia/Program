#include <iostream>
int main(){
    int grade[1000];
    int index = 0;
    for (size_t i = 0; i < 1000; i++)
    {
        scanf("%d",grade+i);
        index++;
        if(grade[i] == 0) break;
    }
    int res = 0;
    int cache = 0;
    for (size_t i = 0; i < index; i++)
    {
        if(grade[i] == 1) res += 1,cache = 0;
        if(grade[i] == 2) res += 2,res += cache,cache+=2;
        if(grade[i] == 0) break;
    }
    printf("%d",res);
    return 0;
}