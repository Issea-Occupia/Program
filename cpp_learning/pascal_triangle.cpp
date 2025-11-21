#include <iostream>
int combination(int i,int j){
    if (i>j||i<0||j<0)
    {
        return -1;
    }
    if (i == j||i == 0)
    {
        return 1;
    }
    if (i == 1)
    {
        return j;
    }
    return combination(i-1,j-1)+combination(i,j-1);
}
int main(){
    int n = 0;
    std::cin >> n;
    int i = 0;
    while(i < n){
        int j = 0;
        while(j <= i){
            int k = combination(j,i);
            std::cout << k <<" ";
            j++;
        }
        std::cout <<std::endl;
        i++;
    }
    return 0;
}