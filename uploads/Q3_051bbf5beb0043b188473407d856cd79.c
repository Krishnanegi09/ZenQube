#include <stdio.h>
int main()
{
    char name[8];
    printf("Enter your name: ");
    scanf("%s", name); // No length specifier!
    printf("Hello %s!\n", name);
    return 0;
}