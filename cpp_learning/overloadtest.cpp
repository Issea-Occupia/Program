#include <iostream>
#include <string>
template <typename ...Args>
void print(Args...args);
template <int ... Args>
void print();
template <typename T1 , typename T2>
auto add(T1 a,T2 b){
    return a+b;
}
int main(){
    print(1,'\n',12,333);
    print(1,"hello",5554);
    print<1,55,3335,8>();
    auto a = add(3,133.2);
    std::cout << a;
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