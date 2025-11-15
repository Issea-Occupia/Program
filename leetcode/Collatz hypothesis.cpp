#include<iostream>
int main(){
    using namespace std;
    int count = 0;
    int num;
    cin >> num;
    while(num != 1){
        if(num % 2 == 0) {num /= 2;count ++;}
        else {num = num*3 + 1;count ++;} 
    }
    cout << count;
    return 0;
}