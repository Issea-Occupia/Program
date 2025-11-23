#include "../include/Array.h"
#include <iostream>
int main(){
    Array<int> *a = new Array<int>(10);
    a[0] = 10;
    Array<int> b = *a;
    b[0] = 20;
    std::cout << (*a)[0];
    return 0;
}