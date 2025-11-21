#ifndef STACK_H
#define STACK_H
class Stack {
    private:
        static const int MAX = 10;
        int container[MAX];
        int topindex;
    public:
        Stack();
        ~Stack();
        void push(int);
        int pop();
        int top();
        bool isempty();
        int size();
};
#endif // STACK_H