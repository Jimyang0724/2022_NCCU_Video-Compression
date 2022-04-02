cmake_minimum_required(VERSION 2.8)
project(HW1)
include_directories(include)
file(GLOB SOURCES "src/*.cpp")
# file(GLOB SOURCES "src/main.cpp")
find_package(OpenCV REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(hw1.exe ${SOURCES})
target_link_libraries(hw1.exe ${OpenCV_LIBS})