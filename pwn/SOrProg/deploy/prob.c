#include <unistd.h>

__asm__(
    ".global syscall_gadget\n"
    "syscall_gadget:\n"
    "    syscall\n"
    "    ret\n"
);

char g[0x400];

void vuln(void) {
    char buf[16];
    read(0, buf, 296);
    read(0, buf, 296);
}

int main(void) {
    vuln();
    return 0;
}
