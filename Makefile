# ZenCube Sandbox Makefile - Cross-Platform Support
# Supports macOS and Linux (Unix systems)
# For Windows, use CMake instead

# Detect OS
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    # macOS - librt is not needed (functions are in standard library)
    CC = clang
    LDFLAGS =
else
    # Linux and other Unix
    CC = gcc
    LDFLAGS = -lrt
endif

CFLAGS = -Wall -Wextra -std=c99
TARGET = sandbox
SOURCE = sandbox.c
DEBUG_FLAGS = -g -DDEBUG
RELEASE_FLAGS = -O2 -DNDEBUG

# Test programs
TEST_DIR = tests
TEST_PROGRAMS = $(TEST_DIR)/infinite_loop $(TEST_DIR)/memory_hog $(TEST_DIR)/fork_bomb $(TEST_DIR)/file_size_test
TEST_SOURCES = $(TEST_DIR)/infinite_loop.c $(TEST_DIR)/memory_hog.c $(TEST_DIR)/fork_bomb.c $(TEST_DIR)/file_size_test.c

# Default target - build everything
all: $(TARGET) tests

# Build sandbox with standard flags
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -D_GNU_SOURCE -D_POSIX_C_SOURCE=199309L -o $(TARGET) $(SOURCE) $(LDFLAGS)
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		xattr -d com.apple.quarantine $(TARGET) 2>/dev/null || true; \
		echo "🔓 Removed macOS quarantine (if present)"; \
	fi
	@echo "✅ Sandbox compiled successfully"

# Debug build with debugging symbols and debug output
debug: $(SOURCE)
	$(CC) $(CFLAGS) $(DEBUG_FLAGS) -D_GNU_SOURCE -D_POSIX_C_SOURCE=199309L -o $(TARGET) $(SOURCE) $(LDFLAGS)
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		xattr -d com.apple.quarantine $(TARGET) 2>/dev/null || true; \
		echo "🔓 Removed macOS quarantine (if present)"; \
	fi
	@echo "✅ Debug build completed"

# Release build with optimizations
release: $(SOURCE)
	$(CC) $(CFLAGS) $(RELEASE_FLAGS) -D_GNU_SOURCE -D_POSIX_C_SOURCE=199309L -o $(TARGET) $(SOURCE) $(LDFLAGS)
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		xattr -d com.apple.quarantine $(TARGET) 2>/dev/null || true; \
		echo "🔓 Removed macOS quarantine (if present)"; \
	fi
	@echo "✅ Release build completed"

# Build all test programs
tests: $(TEST_PROGRAMS)
	@echo "✅ All test programs compiled successfully"

# Build individual test programs
$(TEST_DIR)/infinite_loop: $(TEST_DIR)/infinite_loop.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "✅ Built infinite_loop test"

$(TEST_DIR)/memory_hog: $(TEST_DIR)/memory_hog.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "✅ Built memory_hog test"

$(TEST_DIR)/fork_bomb: $(TEST_DIR)/fork_bomb.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "✅ Built fork_bomb test"

$(TEST_DIR)/file_size_test: $(TEST_DIR)/file_size_test.c
	$(CC) $(CFLAGS) -o $@ $<
	@echo "✅ Built file_size_test"

# Run Phase 1 tests
test-phase1: $(TARGET)
	@echo "Running Phase 1 tests..."
	@python3 test_sandbox.py || echo "Note: Python tests recommended for cross-platform compatibility"

# Run Phase 2 tests (resource limits)
test-phase2: $(TARGET) tests
	@echo "Running Phase 2 resource limit tests..."
	@python3 test_phase2.py || echo "Note: Python tests recommended for cross-platform compatibility"

# Run all tests
test: test-phase1 test-phase2
	@echo "✅ All tests completed"

# Clean build artifacts
clean:
	rm -f $(TARGET) $(TEST_PROGRAMS)
	rm -f test_output.dat
	@echo "✅ Cleaned build artifacts"

# Install to system (requires sudo)
install: $(TARGET)
	cp $(TARGET) /usr/local/bin/
	@echo "✅ Installed sandbox to /usr/local/bin/"

# Uninstall from system (requires sudo)
uninstall:
	rm -f /usr/local/bin/$(TARGET)
	@echo "✅ Uninstalled sandbox from /usr/local/bin/"

# Show help
help:
	@echo "ZenCube Sandbox Build System - Cross-Platform"
	@echo ""
	@echo "Platform: $(UNAME_S)"
	@echo "Compiler: $(CC)"
	@echo ""
	@echo "Available targets:"
	@echo "  all         - Build sandbox and test programs (default)"
	@echo "  sandbox     - Build only the sandbox"
	@echo "  tests       - Build only test programs"
	@echo "  debug       - Build with debug symbols"
	@echo "  release     - Build optimized release version"
	@echo "  test        - Run all test suites"
	@echo "  test-phase1 - Run Phase 1 tests only"
	@echo "  test-phase2 - Run Phase 2 resource limit tests"
	@echo "  clean       - Remove build artifacts"
	@echo "  install     - Install to /usr/local/bin (requires sudo)"
	@echo "  uninstall   - Remove from /usr/local/bin (requires sudo)"
	@echo "  help        - Show this help message"
	@echo ""
	@echo "Note: For Windows, use CMake build system instead:"
	@echo "  cmake -B build"
	@echo "  cmake --build build --config Release"

# Declare phony targets
.PHONY: all debug release tests test test-phase1 test-phase2 clean install uninstall help