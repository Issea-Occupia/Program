#include <iostream>
#include <string>
template <typename ...Args>
void print(Args... args);
int main(){
    std::string str_1 = "hello";
    std::string str_2 = " hi";
    print(str_1);
    print(115);
    print(12,334);
    return 0;
}
template <typename ...Args>
void print(Args... args){
    (std::cout << ... << args);
    std::cout << std::endl;
}