#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main() {
    unsigned char type = 1;
    int size = 10;
    char* buf = malloc(15);
    char test[] = "abcdefghi";
    memcpy(buf, &type, 1);
    memcpy(buf + 1, &size, 4);
    memcpy(buf + 5, test, 10);
    int fd = open("output", O_RDWR);
    write(fd, buf, 15);
    return 0;
}
