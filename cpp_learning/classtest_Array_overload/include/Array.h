#ifndef ARRAY_H_
#define ARRAY_H_
#include <cstdlib>
template <typename T>
class Array
{
private:
    T *data;
    size_t size;
    
public:
    Array(size_t size);
    ~Array();
    size_t size();

};
#endif //ARRAY_H_