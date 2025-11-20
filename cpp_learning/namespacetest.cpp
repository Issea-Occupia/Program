#include <iostream>
namespace parent{
    namespace child{
        void displayMessage() {
            std::cout << "Hello from the nested namespace!" << std::endl;
        }
    }
}
int main() {
    parent::child::displayMessage();
    using namespace parent;
    child::displayMessage();
    using namespace child;
    displayMessage();
    return 0;
}