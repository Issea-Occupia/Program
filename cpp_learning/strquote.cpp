#include <iostream>
#include <string>
const std::string & multiple(std::string & str);
int main(){
    std::string str_1;
    std::cout << "input some string:" << std::endl;
    std::getline(std::cin,str_1);
    multiple(str_1);
    std::cout << str_1;
    return 0;
}
const std::string & multiple(std::string & str){
    str = str + str;
    return str;
}

