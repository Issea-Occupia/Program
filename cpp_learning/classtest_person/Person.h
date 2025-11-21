#ifndef PERSON_H
#define PERSON_H
#include <string>
#include <iostream>
class Person {
private:
    std::string name;
    int age;
    double height;
    void privateMethod();
    void initgreet(const std::string& name) {
        std::cout << "Hello, " << name << " !" << std::endl;
    };
public:
    Person();
    Person(const std::string& name, int age, double height) ;
    ~Person() ;
    std::string getName() const;
    int getAge() const;
    double getHeight() const;
    void introduction() const;
    void callPrivateMethod();
    
};
#endif // PERSON_H