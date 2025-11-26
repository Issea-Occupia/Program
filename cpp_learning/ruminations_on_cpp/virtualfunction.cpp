#include<string>
#include<iostream>
class Person{
    public:
        std::string name;
        virtual void greet() {std::cout << name <<std::endl;}
        Person(std::string n): name(n) {}
        virtual ~Person() = default;
};

class Teto:virtual public Person{
    public:
        Teto(std::string n):Person(n){};
        void greet() override {std::cout << name << std::endl;}

};

class Miku:public Teto,public Person{
    public:
        Miku():Person("Miku"){};
        void greet() override {std::cout << name <<std::endl;}
};



int main(){
    Person *p = new Miku();
    p->greet();
    return 0;
}