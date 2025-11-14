cmake_minimum_required(VERSION 3.10)
project(ZenCube VERSION 2.0)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Platform-specific settings
if(WIN32)
    # Windows-specific settings
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    set(PLATFORM_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/sandbox.c)
else()
    # Unix/Linux/macOS settings
    add_definitions(-D_GNU_SOURCE -D_POSIX_C_SOURCE=199309L)
    # macOS doesn't have librt (functions are in standard library)
    if(NOT APPLE)
        find_library(RT_LIBRARY rt)
        if(RT_LIBRARY)
            link_libraries(${RT_LIBRARY})
        endif()
    endif()
endif()

# Build main sandbox executable
add_executable(sandbox ${CMAKE_CURRENT_SOURCE_DIR}/sandbox.c)

# Compiler warnings
if(MSVC)
    target_compile_options(sandbox PRIVATE /W4)
else()
    target_compile_options(sandbox PRIVATE -Wall -Wextra)
endif()

# Build test programs
add_executable(tests_infinite_loop ${CMAKE_CURRENT_SOURCE_DIR}/tests/infinite_loop.c)
add_executable(tests_memory_hog ${CMAKE_CURRENT_SOURCE_DIR}/tests/memory_hog.c)
add_executable(tests_fork_bomb ${CMAKE_CURRENT_SOURCE_DIR}/tests/fork_bomb.c)
add_executable(tests_file_size_test ${CMAKE_CURRENT_SOURCE_DIR}/tests/file_size_test.c)

# Set output directories
set_target_properties(sandbox PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

set_target_properties(tests_infinite_loop tests_memory_hog tests_fork_bomb tests_file_size_test PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests
)

# Copy test executables to tests directory with expected names
if(UNIX)
    set(TEST_DIR "${CMAKE_BINARY_DIR}/tests")
    add_custom_command(TARGET tests_infinite_loop POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${TEST_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:tests_infinite_loop> ${TEST_DIR}/infinite_loop
    )
    add_custom_command(TARGET tests_memory_hog POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${TEST_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:tests_memory_hog> ${TEST_DIR}/memory_hog
    )
    add_custom_command(TARGET tests_fork_bomb POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${TEST_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:tests_fork_bomb> ${TEST_DIR}/fork_bomb
    )
    add_custom_command(TARGET tests_file_size_test POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${TEST_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:tests_file_size_test> ${TEST_DIR}/file_size_test
    )
endif()

# Install targets
install(TARGETS sandbox
    RUNTIME DESTINATION bin
)

# Print build information
message(STATUS "Building ZenCube Sandbox")
message(STATUS "Platform: ${CMAKE_SYSTEM_NAME}")
message(STATUS "C Compiler: ${CMAKE_C_COMPILER_ID}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
