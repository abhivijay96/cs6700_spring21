cmake_minimum_required (VERSION 2.8.11)
project (generate)

file(GLOB SOURCES "./*.cpp")
add_executable (generate ${SOURCES})