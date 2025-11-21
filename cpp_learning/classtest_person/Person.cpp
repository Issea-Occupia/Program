#include "Person.h"
#include <iostream>
Person::Person(const std::string& name, int age, double height) : name(name), age(age), height(height) {Person::initgreet(name);}
Person::Person() : name(""), age(0), height(0.0) {std::cout << "Default constructor called." << std::endl;}
std::string Person::getName() const {
    return name;
}

int Person::getAge() const {
    return age;
}

double Person::getHeight() const {
    return height;
}

void Person::introduction() const {
    std::cout << "Hello, my name is " << name << ", I am " << age << " years old and " << height << " meters tall." << std::endl;
}

void Person::privateMethod() {
    std::cout << "This is a private method." << std::endl;
    initgreet(name);
}

void Person::callPrivateMethod() {
    std::cout << "you're calling a private method:" << std::endl;
    privateMethod();
}

Person::~Person() {
    std::cout << "Goodbye , " << name << std::endl;
}