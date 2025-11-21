#include "Person.h"
#include <iostream>
int main() {
    Person* person = new Person("Alice", 30,1.76);
    std::cout << "Name: " << person->getName() << std::endl;
    std::cout << "Age: " << person->getAge() << std::endl;
    std::cout << "Height: " << person->getHeight() << std::endl;
    person->introduction();
    person->callPrivateMethod();
    person->~Person();
    new (person) Person();
    return 0;
}