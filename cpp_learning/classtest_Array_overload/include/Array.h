#ifndef ARRAY_H_
#define ARRAY_H_
#include<cstdlib>

template<typename T>
class Array {
private:
    T* data;
    size_t n;
    size_t idx;

public:
    Array(size_t n)
        : data(new T[n]), n(n)
    {}

    Array(const Array<T>& other){
        int len = other.length();
        this->n = len;
        this->data = new T[len];
        for (size_t i = 0; i < len; i++)
        {
            this->data[i] = other.data[i];
        }
    }

    void push_back(const T& _data){
        if(idx + 1 == n){
            T* temp = new T[2*n];
            for (size_t i = 0; i < n; i++)
            {
                temp[i] = this->data[i];
            }
            temp[n] = _data;
            n *= 2;
            delete[] data;
            data = temp;
            idx++;
        }else {
            this->data[++idx] = _data;
        }
    }

    void reverse(){
        T* temp = new T[idx + 1];
        for (size_t i = 0; i <= idx; i++)
        {
            temp[i] = this->data[idx - i];
        }
        delete[] data;
        data = temp;
    }

    Array()
        : data(nullptr), n(0)
    {}

    Array<T>& operator=(const Array<T>& other){
        if(this == &other) return *this;//防止自拷贝
        delete[] this->data;//释放内存
        int len = other.length();
        this->n = len;
        this->data = new T[len];
        for (size_t i = 0; i < len; i++)
        {
            this->data[i] = other.data[i];
        }
        return *this;//引用类型实质是对象，必须解引用。
    }

    ~Array() {
        delete[] data;
    }

    size_t length() const {
        return n;
    }

    T& operator[](size_t index) {
        return *(data + index);
    }

};

#endif // ARRAY_H_
