cmake_minimum_required(VERSION 3.10)

project(classtest_stack)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_executable(classtest_stack
    src/main.cpp
    src/stack.cpp
)
