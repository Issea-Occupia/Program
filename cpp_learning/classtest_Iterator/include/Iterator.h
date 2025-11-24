#ifndef ITERATOR_H_
#define ITERATOR_H_

template <typename T>
class Iterator
{
private:
    /* data */
public:
    Iterator(T* p):ptr(p){};
    ~Iterator();
};


#endif  //ITERATOR_H_