#include<iostream>
using namespace std;
int isprime(int num);
int main(){
    int num;
    cin >> num;
    int max = 2;
    int min = num;
    for (size_t a = 1; a < num; a++)
    {
        int b = num - a;
        int flag_a = isprime(a);
        int flag_b = isprime(b);
        if(flag_a == 1 && flag_b == 1){
            max = a;
            min = b;
        }
    }
    cout << min <<" "<< max;
    return 0;
}
int isprime(int num){
    int flag = 1;
    if(num == 1) return 0;
    for(int i =2;i < num; i++){
        if(num % i == 0) flag = 0;
    }
    return flag;
}