#include<stdio.h>
#include<math.h>
void main()
{
    int n , ld = 0, count = 0, dup = 0, sum = 0;
    scanf(" %d", &n);
    dup = n;
    int temp = n;
    while(temp != 0){
        temp = temp/10;
        count++;
    }
    n = dup;
    while(n > 0){
        ld = n % 10;
        sum = sum + pow(ld,count);
        n = n / 10;
    }
    if (sum == dup)
    {
        printf("ARMSTRONG");
    }
    else
    printf("NOT ARMSTRONG");
    
}