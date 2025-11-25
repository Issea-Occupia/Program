cmake_minimum_required(VERSION 3.16)
project(NcmWinDecoder LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 找 OpenSSL
find_package(OpenSSL REQUIRED)

add_executable(NcmWinDecoder
    src/main.cpp
    src/ui.cpp
    src/ncm_decoder.cpp
)

target_include_directories(NcmWinDecoder PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party
)

target_link_libraries(NcmWinDecoder PRIVATE
    OpenSSL::SSL
    OpenSSL::Crypto
)

# Windows 子系统，不弹控制台
if (MSVC)
    set_target_properties(NcmWinDecoder PROPERTIES LINK_FLAGS "/SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")
endif()
