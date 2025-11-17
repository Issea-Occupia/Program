#include <iostream>
#include <fstream>
#include <string>
int main(){
    using std::ifstream;
    ifstream fin;
    fin.open("output.txt");
    int num;
    std::string str;
    fin>>num;
    fin.get();
    std::getline(fin,str);
    std::cout<<num<<std::endl<<str<<std::endl;
    fin.close();
    return 0;
}
