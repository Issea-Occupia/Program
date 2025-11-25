#include <iostream>
class Trace{
    public:
        void print(char * c){std::cout << c;};

    private:
        int noisy;
        
};


int main(){
    Trace t;
    t.print("hello");
    return 0;
}