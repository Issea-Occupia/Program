#include <iostream>
#include <string>
class Human{
    public:

    Human(int a, bool g, double h, std::string n): age(a), gender(g), height(h), name(n) {}
    virtual ~Human(){};
    virtual void introduce(){}

    protected:

    int age;
    bool gender;//0-female,1-male
    double height;
    std::string name;
};


class Asia:public Human{
    public:
    Asia(){};
    Asia(int a,bool b,double c,std::string d):Human(a,b,c,d){
        std::cout << "An Aisan is created!" <<std::endl;
    };

    void introduce() override{
        std::cout << "I'm an Asian,aged: " << age <<" and I'm a" <<(gender?" male":" female") << " I'm " << height << " high," << "nice to meet you !" << std::endl;
    }
};
class HumanSurrogate{
    public:

    HumanSurrogate(Human & hp): ph(&hp){};
    void introduce() {
        ph->introduce();
    }

    private:
    Human* ph = nullptr;

};