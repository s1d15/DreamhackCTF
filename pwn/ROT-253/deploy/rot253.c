// Name: rot253.c
// Compile: gcc -fno-stack-protector rot253.c -o rot253 ; strip rot253
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MENU_ENCRYPTION 1
#define MENU_DECRYPTION 2

int rot253(uint8_t byte);
int rot253_inv(uint8_t byte);
void my_memcpy(char *dst, char *src, size_t n);
void hxd(uint8_t *mem, size_t n);
void unhexlify(char *output, char *hexstr, size_t len);
void encrypt(char *ct, char *pt);
void decrypt(char *pt, char *ct);
void print_menu();
void foo();

int main(void) {
    char yn[2];

    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    do {
        foo();

        printf("want to quit (y/n)? ");
        read(0, yn, 2);
    } while (yn[0] != 'y');

    return 0;
}

int rot253(uint8_t byte) {  // ROT-253
    char key;

    key = 253;
    return byte + key;
}

int rot253_inv(uint8_t byte) {  // inverse of ROT-253
    char key;

    key = 3;
    return byte + key;
}

void my_memcpy(char *dst, char *src, size_t n) {  // my custom memcpy *_*
    asm volatile(
        "push %rdi; push %rsi; push %rdx; push %rcx;"
        "mov %rdx, %rcx;"
        "rep movsb (%rsi),(%rdi);"
        "pop %rcx; pop %rdx; pop %rsi; pop %rdi"
    );
}

void hxd(uint8_t *mem, size_t n) {
    size_t i;

    for (i = 0; i < n; i++)
        printf("%02x", mem[i]);
    puts("\n");
}

void unhexlify(char *output, char *hexstr, size_t len) {
    int i;

    for (i = 0; i < len / 2; i++)
        sscanf(&hexstr[i * 2], "%2hhx", &output[i]);
}

void encrypt(char *ct, char *pt) {
    size_t len;
    int i;

    memset(pt, 0x00, 128);

    printf("plaintext? ");
    read(0, pt, 153);

    len = strlen(pt);

    my_memcpy(ct, pt, len);

    i = len;
    while (i--)
        ct[i] = rot253(ct[i]);

    printf("ciphertext (hexstr): ");
    hxd(ct, len);
}

void decrypt(char *pt, char *ct) {
    int i;
    char buf[255];
    ssize_t readn;

    memset(ct, 0x00, 128);
    memset(pt, 0x00, 128);

    printf("ciphertext (hexstr)? ");
    readn = read(0, buf, 254);
    if (readn < 1)
        exit(1);

    unhexlify(ct, buf, readn - 1);

    for (i = 0; i < 127; i++)
        pt[i] = rot253_inv(ct[i]);

    printf("plaintext: %s\n", pt);
}

void print_menu() {
    puts(" ===============");
    puts(" = ROT-253 *_* =");
    puts(" ===============");
    puts("1. encrypt");
    puts("2. decrypt");
    printf("> ");
}

void foo() {
    uint8_t menu;
    char pt[128];
    char ct[128];

    do {
        print_menu();
        scanf("%hhu", &menu);

        switch (menu) {
        case MENU_ENCRYPTION:
            encrypt(ct, pt);
            break;
        case MENU_DECRYPTION:
            decrypt(pt, ct);
            break;
        }
    } while (MENU_ENCRYPTION <= menu && menu <= MENU_DECRYPTION);

    memset(pt, 0x00, 144);
    memset(ct, 0x00, 128);
}
