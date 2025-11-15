#include<iostream>
int main(){
    using namespace std;
    int num;
    cin >> num;
    int left = 0;
    for(int i = 0;i < num;i++){
        for(int j = 0;j < i;j++){
            left ++;
        }
    }
    int count = 0;
    for(int i = 1;i < 100000000;i+=2){
        count++;
        if(count > left && count<= left + num) cout << i << " ";
        if(count > left+num) break;
    }
    return 0;
}