#include "../include/stack.h"
Stack::Stack(){
    topindex = 0;
}

Stack::~Stack(){
    
}

void Stack::push(int n){
    if(!(topindex < MAX)) throw  "Stackoverflow";
    container[topindex++] = n;
}

int Stack::pop(){
    if(!(topindex > 0)) throw "Stackempty";
    return container[--topindex];
}

bool Stack::isempty(){
    return topindex == 0;
}

int Stack::size(){
    return topindex;
}

int Stack::top(){
    if(!(topindex > 0)) throw "Stackempty";
    return container[topindex - 1];
}
