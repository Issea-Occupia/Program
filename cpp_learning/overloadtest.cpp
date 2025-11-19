#include <iostream>
#include <string>
template <typename ...Args>
void print(Args...args);
template <int ... Args>
void print();
int main(){
    print(1,12,333);
    print(1,"hello",5554);
    print<1,55,3335,8>();
    return 0;
}
template <typename ...Args>
void print(Args...args){
    (std::cout << ... <<args);
    std::cout << std::endl;
}
template <int ... Args>
void print(){
    (std::cout << (...+Args));
    std::cout << std::endl;
}