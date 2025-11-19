#include <iostream>
int __double(int &num);
int main(){
    int a = 10;
    int b = __double(a);
    std::cout << b;
    std::cout <<std::endl << a;
}
int __double(int &num){
    num *= 2;
    return num*2;
}