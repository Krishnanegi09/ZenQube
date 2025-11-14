#ifndef _WIN32
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#define _POSIX_C_SOURCE 199309L
#endif

#ifdef _WIN32
#include <windows.h>
#include <process.h>
#include <io.h>
#else
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <signal.h>
#include <string.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <stdarg.h>
#include <limits.h>

/**
 * ZenCube Sandbox Runner - Cross-Platform Version
 * 
 * A sandbox implementation with resource limits to prevent runaway processes.
 * Supports CPU time, memory, process count, and file size restrictions.
 * 
 * Platforms: Windows, macOS, Linux
 * 
 * Features:
 * - CPU time limits
 * - Memory limits (where supported)
 * - Process count limits (where supported)
 * - File size limits (where supported)
 * 
 * Author: Systems Programming Team
 * Date: 2025
 */

/* Structure to hold resource limit configuration */
typedef struct {
    int cpu_seconds;      /* CPU time limit in seconds (0 = unlimited) */
    long memory_mb;       /* Memory limit in MB (0 = unlimited) */
    int max_processes;    /* Maximum number of processes (0 = unlimited) */
    long max_file_mb;     /* Maximum file size in MB (0 = unlimited) */
} ResourceLimits;

/* Function prototypes */
void print_usage(const char *program_name);
void log_message(const char *format, ...);
void log_command(int argc, char *argv[], int start_index);

#ifdef _WIN32
double timespec_diff_win32(LARGE_INTEGER *start, LARGE_INTEGER *end);
#else
double timespec_diff(struct timespec *start, struct timespec *end);
#endif

int parse_arguments(int argc, char *argv[], ResourceLimits *limits, int *cmd_start_index);

#ifndef _WIN32
int apply_resource_limits(const ResourceLimits *limits);
void log_resource_limits(const ResourceLimits *limits);
#endif

#ifdef _WIN32
int run_windows(ResourceLimits *limits, int argc, char *argv[], int cmd_start_index);
#else
int run_unix(ResourceLimits *limits, int argc, char *argv[], int cmd_start_index);
#endif

/**
 * Print usage information for the sandbox program
 */
void print_usage(const char *program_name) {
    printf("Usage: %s [OPTIONS] <command> [arguments...]\n", program_name);
    printf("\nDescription:\n");
    printf("  Execute a command in a sandbox with resource limits.\n");
    printf("  The command will run as a child process with enforced constraints.\n");
    printf("\nOptions:\n");
    printf("  --cpu=<seconds>      Limit CPU time (default: unlimited)\n");
    printf("  --mem=<MB>           Limit memory in megabytes (default: unlimited)\n");
    printf("  --procs=<count>      Limit number of processes (default: unlimited)\n");
    printf("  --fsize=<MB>         Limit file size in megabytes (default: unlimited)\n");
    printf("  --help               Display this help message\n");
    printf("\nExamples:\n");
    printf("  %s /bin/ls -l /\n", program_name);
#ifdef _WIN32
    printf("  %s cmd /c dir\n", program_name);
#else
    printf("  %s /bin/echo Hello\n", program_name);
#endif
    printf("  %s --cpu=5 /bin/sleep 10\n", program_name);
    printf("  %s --mem=256 --cpu=10 ./memory_test\n", program_name);
    printf("\nPlatform Notes:\n");
#ifdef _WIN32
    printf("  Windows: Resource limits have limited support.\n");
    printf("  CPU limits are enforced via job objects.\n");
#else
    printf("  Unix/Linux/macOS: Full POSIX resource limit support.\n");
    printf("  Resource Limit Signals:\n");
    printf("    SIGXCPU - CPU time limit exceeded\n");
    printf("    SIGKILL - Memory limit exceeded (kernel kill)\n");
    printf("    SIGXFSZ - File size limit exceeded\n");
#endif
}

/**
 * Log a formatted message with timestamp and sandbox prefix
 */
void log_message(const char *format, ...) {
    va_list args;
    time_t raw_time;
    struct tm *time_info;
    char time_buffer[80];
    
    /* Get current time for logging */
    time(&raw_time);
    time_info = localtime(&raw_time);
    strftime(time_buffer, sizeof(time_buffer), "%H:%M:%S", time_info);
    
    printf("[Sandbox %s] ", time_buffer);
    
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
    
    printf("\n");
    fflush(stdout);
}

/**
 * Log the command being executed with all its arguments
 */
void log_command(int argc, char *argv[], int start_index) {
    printf("[Sandbox] Starting command:");
    for (int i = start_index; i < argc; i++) {
        printf(" %s", argv[i]);
    }
    printf("\n");
    fflush(stdout);
}

#ifdef _WIN32
/**
 * Calculate the difference between two Windows performance counter values
 */
double timespec_diff_win32(LARGE_INTEGER *start, LARGE_INTEGER *end) {
    LARGE_INTEGER frequency;
    QueryPerformanceFrequency(&frequency);
    return (double)(end->QuadPart - start->QuadPart) / (double)frequency.QuadPart;
}
#else
/**
 * Calculate the difference between two timespec structures in seconds
 */
double timespec_diff(struct timespec *start, struct timespec *end) {
    return (end->tv_sec - start->tv_sec) + (end->tv_nsec - start->tv_nsec) / 1000000000.0;
}
#endif

/**
 * Parse command-line arguments and extract resource limits
 * Returns 0 on success, -1 on error
 */
int parse_arguments(int argc, char *argv[], ResourceLimits *limits, int *cmd_start_index) {
    int i = 1;
    
    /* Initialize limits to unlimited (0) */
    limits->cpu_seconds = 0;
    limits->memory_mb = 0;
    limits->max_processes = 0;
    limits->max_file_mb = 0;
    
    /* Parse options */
    while (i < argc && argv[i][0] == '-') {
        if (strcmp(argv[i], "--help") == 0) {
            print_usage(argv[0]);
            exit(EXIT_SUCCESS);
        } else if (strncmp(argv[i], "--cpu=", 6) == 0) {
            limits->cpu_seconds = atoi(argv[i] + 6);
            if (limits->cpu_seconds < 0) {
                fprintf(stderr, "Error: Invalid CPU limit: %s\n", argv[i] + 6);
                return -1;
            }
        } else if (strncmp(argv[i], "--mem=", 6) == 0) {
            limits->memory_mb = atol(argv[i] + 6);
            if (limits->memory_mb < 0) {
                fprintf(stderr, "Error: Invalid memory limit: %s\n", argv[i] + 6);
                return -1;
            }
        } else if (strncmp(argv[i], "--procs=", 8) == 0) {
            limits->max_processes = atoi(argv[i] + 8);
            if (limits->max_processes < 0) {
                fprintf(stderr, "Error: Invalid process limit: %s\n", argv[i] + 8);
                return -1;
            }
        } else if (strncmp(argv[i], "--fsize=", 8) == 0) {
            limits->max_file_mb = atol(argv[i] + 8);
            if (limits->max_file_mb < 0) {
                fprintf(stderr, "Error: Invalid file size limit: %s\n", argv[i] + 8);
                return -1;
            }
        } else {
            fprintf(stderr, "Error: Unknown option: %s\n", argv[i]);
            return -1;
        }
        i++;
    }
    
    *cmd_start_index = i;
    return 0;
}

#ifndef _WIN32
/**
 * Apply resource limits to the current process (Unix/Linux/macOS only)
 * Returns 0 always (warnings are logged but execution continues)
 * Note: On macOS, memory limits may not be fully enforced
 */
int apply_resource_limits(const ResourceLimits *limits) {
    struct rlimit rlim;
    
    /* Apply CPU time limit */
    if (limits->cpu_seconds > 0) {
        rlim.rlim_cur = limits->cpu_seconds;
        rlim.rlim_max = limits->cpu_seconds;
        if (setrlimit(RLIMIT_CPU, &rlim) != 0) {
            fprintf(stderr, "[Sandbox] Error: Failed to set CPU limit: %s\n", strerror(errno));
            return -1;
        }
        log_message("CPU limit set to %d seconds", limits->cpu_seconds);
    }
    
    /* Apply memory limit (address space) */
    if (limits->memory_mb > 0) {
        rlim.rlim_cur = (rlim_t)limits->memory_mb * 1024 * 1024;
        rlim.rlim_max = (rlim_t)limits->memory_mb * 1024 * 1024;
        
        #ifdef __APPLE__
        /* macOS: RLIMIT_AS is not well supported. Log warning but continue */
        if (setrlimit(RLIMIT_AS, &rlim) != 0) {
            log_message("Warning: Memory limit not fully supported on macOS (RLIMIT_AS failed: %s). Continuing without strict memory limit.", strerror(errno));
            /* Don't return error - continue execution */
        } else {
            log_message("Memory limit set to %ld MB (macOS - may have limited enforcement)", limits->memory_mb);
        }
        #else
        /* Linux - use RLIMIT_AS */
        if (setrlimit(RLIMIT_AS, &rlim) != 0) {
            log_message("Warning: Failed to set memory limit: %s. Continuing anyway.", strerror(errno));
            /* Continue execution even if memory limit fails */
        } else {
            log_message("Memory limit set to %ld MB", limits->memory_mb);
        }
        #endif
    }
    
    /* Apply process count limit (Linux only, not available on macOS) */
    if (limits->max_processes > 0) {
#ifdef RLIMIT_NPROC
        rlim.rlim_cur = limits->max_processes;
        rlim.rlim_max = limits->max_processes;
        if (setrlimit(RLIMIT_NPROC, &rlim) != 0) {
            fprintf(stderr, "[Sandbox] Error: Failed to set process limit: %s\n", strerror(errno));
            return -1;
        }
        log_message("Process limit set to %d", limits->max_processes);
#else
        log_message("Warning: Process limit not supported on this platform");
#endif
    }
    
    /* Apply file size limit */
    if (limits->max_file_mb > 0) {
        rlim.rlim_cur = (rlim_t)limits->max_file_mb * 1024 * 1024;
        rlim.rlim_max = (rlim_t)limits->max_file_mb * 1024 * 1024;
        if (setrlimit(RLIMIT_FSIZE, &rlim) != 0) {
            fprintf(stderr, "[Sandbox] Error: Failed to set file size limit: %s\n", strerror(errno));
            return -1;
        }
        log_message("File size limit set to %ld MB", limits->max_file_mb);
    }
    
    return 0;
}

/**
 * Log the active resource limits (Unix/Linux/macOS only)
 */
void log_resource_limits(const ResourceLimits *limits) {
    if (limits->cpu_seconds > 0 || limits->memory_mb > 0 || 
        limits->max_processes > 0 || limits->max_file_mb > 0) {
        printf("[Sandbox] Active resource limits:\n");
        if (limits->cpu_seconds > 0) {
            printf("  CPU Time: %d seconds\n", limits->cpu_seconds);
        }
        if (limits->memory_mb > 0) {
            printf("  Memory: %ld MB\n", limits->memory_mb);
        }
        if (limits->max_processes > 0) {
            printf("  Processes: %d\n", limits->max_processes);
        }
        if (limits->max_file_mb > 0) {
            printf("  File Size: %ld MB\n", limits->max_file_mb);
        }
    } else {
        printf("[Sandbox] No resource limits applied (unlimited)\n");
    }
}
#endif

#ifdef _WIN32
/**
 * Windows implementation using CreateProcess and Job Objects
 */
int run_windows(ResourceLimits *limits, int argc, char *argv[], int cmd_start_index) {
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    HANDLE hJob = NULL;
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION jeli;
    LARGE_INTEGER start_time, end_time, frequency;
    DWORD exit_code;
    double execution_time;
    
    /* Initialize structures */
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));
    
    /* Get start time */
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start_time);
    
    /* Create job object for resource limits */
    if (limits->cpu_seconds > 0 || limits->memory_mb > 0) {
        hJob = CreateJobObject(NULL, NULL);
        if (hJob == NULL) {
            fprintf(stderr, "[Sandbox] Error: Failed to create job object: %lu\n", GetLastError());
            return EXIT_FAILURE;
        }
        
        ZeroMemory(&jeli, sizeof(jeli));
        
        /* Set CPU time limit */
        if (limits->cpu_seconds > 0) {
            jeli.BasicLimitInformation.LimitFlags |= JOB_OBJECT_LIMIT_JOB_TIME;
            jeli.BasicLimitInformation.PerJobUserTimeLimit.QuadPart = 
                limits->cpu_seconds * 10000000LL; /* Convert to 100-nanosecond intervals */
            log_message("CPU limit set to %d seconds (Windows Job Object)", limits->cpu_seconds);
        }
        
        /* Set memory limit */
        if (limits->memory_mb > 0) {
            jeli.BasicLimitInformation.LimitFlags |= JOB_OBJECT_LIMIT_PROCESS_MEMORY;
            jeli.ProcessMemoryLimit = limits->memory_mb * 1024 * 1024;
            log_message("Memory limit set to %ld MB (Windows Job Object)", limits->memory_mb);
        }
        
        if (!SetInformationJobObject(hJob, JobObjectExtendedLimitInformation, &jeli, sizeof(jeli))) {
            fprintf(stderr, "[Sandbox] Error: Failed to set job object limits: %lu\n", GetLastError());
            CloseHandle(hJob);
            return EXIT_FAILURE;
        }
    }
    
    /* Build command line */
    char *cmdline = NULL;
    size_t cmdline_len = 0;
    for (int i = cmd_start_index; i < argc; i++) {
        cmdline_len += strlen(argv[i]) + 3; /* +3 for quotes and space */
    }
    cmdline = (char *)malloc(cmdline_len + 1);
    if (!cmdline) {
        fprintf(stderr, "[Sandbox] Error: Failed to allocate memory\n");
        if (hJob) CloseHandle(hJob);
        return EXIT_FAILURE;
    }
    
    cmdline[0] = '\0';
    for (int i = cmd_start_index; i < argc; i++) {
        if (i > cmd_start_index) strcat(cmdline, " ");
        strcat(cmdline, "\"");
        strcat(cmdline, argv[i]);
        strcat(cmdline, "\"");
    }
    
    /* Create process */
    if (!CreateProcessA(NULL, cmdline, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        fprintf(stderr, "[Sandbox] Error: Failed to create process: %lu\n", GetLastError());
        free(cmdline);
        if (hJob) CloseHandle(hJob);
        return EXIT_FAILURE;
    }
    
    log_message("Child process created (PID: %lu)", pi.dwProcessId);
    
    /* Assign process to job object */
    if (hJob) {
        if (!AssignProcessToJobObject(hJob, pi.hProcess)) {
            fprintf(stderr, "[Sandbox] Warning: Failed to assign process to job: %lu\n", GetLastError());
        }
    }
    
    /* Wait for process to complete */
    WaitForSingleObject(pi.hProcess, INFINITE);
    
    /* Get end time */
    QueryPerformanceCounter(&end_time);
    execution_time = timespec_diff_win32(&start_time, &end_time);
    
    /* Get exit code */
    GetExitCodeProcess(pi.hProcess, &exit_code);
    
    if (exit_code == STILL_ACTIVE) {
        /* Process was terminated */
        log_message("Process terminated by system");
        exit_code = EXIT_FAILURE;
    } else if (exit_code == 0xFFFFFFFF) {
        /* Check if terminated by job object */
        DWORD reason = 0;
        if (hJob && QueryInformationJobObject(hJob, JobObjectBasicUIRestrictions, &reason, sizeof(reason), NULL)) {
            log_message("Process terminated by job object limits");
        } else {
            log_message("Process exited with status %lu", exit_code);
        }
        exit_code = EXIT_FAILURE;
    } else {
        log_message("Process exited normally with status %lu", exit_code);
    }
    
    log_message("Execution time: %.3f seconds", execution_time);
    
    /* Cleanup */
    free(cmdline);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    if (hJob) CloseHandle(hJob);
    
    return (int)exit_code;
}
#else
/**
 * Unix/Linux/macOS implementation using fork/execvp
 */
int run_unix(ResourceLimits *limits, int argc __attribute__((unused)), char *argv[], int cmd_start_index) {
    pid_t child_pid;
    int status;
    struct timespec start_time, end_time;
    double execution_time;
    
    /* Log resource limits */
    log_resource_limits(limits);
    
    /* Record start time */
    if (clock_gettime(CLOCK_MONOTONIC, &start_time) == -1) {
        log_message("Warning: Failed to get start time: %s", strerror(errno));
    }
    
    /* Create child process using fork() */
    child_pid = fork();
    
    if (child_pid == -1) {
        /* Fork failed */
        fprintf(stderr, "[Sandbox] Error: Failed to create child process: %s\n", 
                strerror(errno));
        return EXIT_FAILURE;
    }
    
    if (child_pid == 0) {
        /* This is the child process */
        log_message("Child process created (PID: %d)", getpid());
        
        /* Apply resource limits in child process */
        /* Note: apply_resource_limits may log warnings but won't fail on macOS for memory limits */
        apply_resource_limits(limits);
        
        /* Replace process image with target command using execvp() */
        if (execvp(argv[cmd_start_index], &argv[cmd_start_index]) == -1) {
            /* execvp() failed */
            fprintf(stderr, "[Sandbox] Child Error: Failed to execute '%s': %s\n", 
                    argv[cmd_start_index], strerror(errno));
            exit(EXIT_FAILURE);
        }
        
        /* This line should never be reached if execvp() succeeds */
        exit(EXIT_FAILURE);
    } else {
        /* This is the parent process */
        log_message("Child PID: %d", child_pid);
        
        /* Wait for child process to complete */
        pid_t wait_result = waitpid(child_pid, &status, 0);
        
        /* Record end time */
        if (clock_gettime(CLOCK_MONOTONIC, &end_time) == -1) {
            log_message("Warning: Failed to get end time: %s", strerror(errno));
            execution_time = -1.0;
        } else {
            execution_time = timespec_diff(&start_time, &end_time);
        }
        
        if (wait_result == -1) {
            fprintf(stderr, "[Sandbox] Error: waitpid() failed: %s\n", strerror(errno));
            return EXIT_FAILURE;
        }
        
        /* Analyze and log child process exit status */
        if (WIFEXITED(status)) {
            /* Child exited normally */
            int exit_code = WEXITSTATUS(status);
            log_message("Process exited normally with status %d", exit_code);
            
            if (execution_time >= 0) {
                log_message("Execution time: %.3f seconds", execution_time);
            }
            
            return exit_code;
        } else if (WIFSIGNALED(status)) {
            /* Child was terminated by a signal */
            int signal_num = WTERMSIG(status);
            /* Note: strsignal() is not available on all platforms (e.g., macOS) */
            log_message("Process terminated by signal %d", signal_num);
            
            /* Provide specific information for resource limit signals */
            if (signal_num == SIGXCPU) {
                log_message("⚠️  RESOURCE LIMIT VIOLATED: CPU time limit exceeded");
                log_message("The process used more CPU time than allowed (%d seconds)", 
                           limits->cpu_seconds);
            } else if (signal_num == SIGKILL) {
                log_message("⚠️  Process was killed (possibly by memory limit)");
                if (limits->memory_mb > 0) {
                    log_message("Memory limit was set to %ld MB", limits->memory_mb);
                }
            } else if (signal_num == SIGXFSZ) {
                log_message("⚠️  RESOURCE LIMIT VIOLATED: File size limit exceeded");
                if (limits->max_file_mb > 0) {
                    log_message("File size limit was set to %ld MB", limits->max_file_mb);
                }
            }
            
            if (execution_time >= 0) {
                log_message("Execution time before termination: %.3f seconds", execution_time);
            }
            
#ifdef WCOREDUMP
            if (WCOREDUMP(status)) {
                log_message("Core dump was created");
            }
#endif
            
            return EXIT_FAILURE;
        } else if (WIFSTOPPED(status)) {
            /* Child was stopped */
            int stop_signal = WSTOPSIG(status);
            log_message("Process stopped by signal %d", stop_signal);
            return EXIT_FAILURE;
        } else {
            /* Unknown status */
            log_message("Process ended with unknown status: %d", status);
            return EXIT_FAILURE;
        }
    }
}
#endif

/**
 * Main sandbox runner function
 */
int main(int argc, char *argv[]) {
    ResourceLimits limits;
    int cmd_start_index;
    
    /* Parse command line arguments and resource limits */
    if (parse_arguments(argc, argv, &limits, &cmd_start_index) != 0) {
        fprintf(stderr, "\n");
        print_usage(argv[0]);
        return EXIT_FAILURE;
    }
    
    /* Check if command is specified */
    if (cmd_start_index >= argc) {
        fprintf(stderr, "Error: No command specified\n\n");
        print_usage(argv[0]);
        return EXIT_FAILURE;
    }
    
    /* Log the command we're about to execute */
    log_command(argc, argv, cmd_start_index);
    
#ifdef _WIN32
    return run_windows(&limits, argc, argv, cmd_start_index);
#else
    return run_unix(&limits, argc, argv, cmd_start_index);
#endif
}