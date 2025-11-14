#!/usr/bin/env python3
"""
Simple interactive program for ZenCube sandbox demos.
Shows standard I/O behaviour and basic computation.
"""

import time


def main():
    print("👋 Hello from ZenCube sample program!")
    name = input("What's your name? ")
    print(f"Nice to meet you, {name}.")

    print("\nLet me crunch a few numbers while you watch...")
    total = 0
    for i in range(1, 6):
        total += i
        print(f" step {i}: running total = {total}")
        time.sleep(0.5)

    print("\n✅ Done! Try editing this file and re-running inside the sandbox.")


if __name__ == "__main__":
    main()



