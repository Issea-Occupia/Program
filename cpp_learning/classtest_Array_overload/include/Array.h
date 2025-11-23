#ifndef ARRAY_H_
#define ARRAY_H_

#include <cstddef>

template<typename T>
class Array {
private:
    T* data;
    size_t n;

public:
    Array(size_t n)
        : data(new T[n]), n(n)
    {}

    ~Array() {
        delete[] data;
    }

    size_t length() const {
        return n;
    }

    T& operator[](size_t index) {
        return *(data + index);
    }

    Array<T>& operator=(const Array<T>& other){
         
    }
};

#endif // ARRAY_H_
