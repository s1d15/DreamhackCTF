#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

size_t dna;
enum life_type {
    NONE,
    EGG,
    CHICKEN
};

typedef struct life {
    void *spirit;
    enum life_type type;
} Life;

typedef struct chicken {
    char name[16];
} Chicken;

typedef struct egg {
    char name[8];
    void (*hatch)(Life *life);
} Egg;

void hatch_egg(Life *life);

void create_egg(Life *life) {
    if (life->type != NONE) {
        printf("Already Generated\n");
        return;
    }
    Egg *e = (Egg *) malloc(sizeof(Egg));
    strncpy(e->name, "bob", sizeof(e->name));
    e->hatch = (((size_t) &hatch_egg ^ dna) << 12) | (((size_t) &hatch_egg ^ dna) >> (64 - 12));
    life->spirit = e;
    life->type = EGG;
    printf("Egg created!\n");
}

void rename_egg(Life *life) {
    if (life->type != EGG) {
        printf("Not an Egg!\n");
        return;
    }
    Egg *egg = life->spirit;
    printf("Enter egg name: ");
    read(STDIN_FILENO, egg->name, sizeof(egg->name));
}

void rename_chicken(Life *life) {
    if (life->type != CHICKEN) {
        printf("Not a Chicken!\n");
        return;
    }
    Chicken *c = life->spirit;
    printf("Enter chicken name: ");
    read(STDIN_FILENO, c->name, sizeof(c->name));
}

void print_egg(Life *life) {
    if (life->type != EGG) {
        printf("Not an Egg!\n");
        return;
    }
    Egg *egg = life->spirit;
    printf("Egg name: %s\n", egg->name);
}

void print_chicken(Life *life) {
    if (life->type != CHICKEN) {
        printf("Not a Chicken!\n");
        return;
    }
    Chicken *c = life->spirit;
    printf("Chicken name: %s\n", c->name);
}

void observe_egg(Life *life) {
    Egg *egg = life->spirit;
    void (*action)(Life *) = (void (*)(Life *)) (((((size_t) egg->hatch) >> 12) | (((size_t) egg->hatch) << (64 - 12))) ^ dna);
    action(life);
}


void hatch_egg(Life *life) {
    free(life->spirit);
    Chicken *c = (Chicken *) malloc(sizeof(Chicken));
    strncpy(c->name, "alice", sizeof(c->name));
    life->spirit = c;
    life->type = CHICKEN;
    printf("Egg hatched!\n");
};


void win() {
    system("/bin/sh");
}


void init_binary() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    FILE *fp;
    fp = fopen("/dev/urandom", "rb");
    fread(&dna, 8, 1, fp);
    fclose(fp);
}

void menu() {
    printf("1. create egg\n");
    printf("2. rename egg\n");
    printf("3. print egg\n");
    printf("4. observe egg\n");
    printf("5. rename chicken\n");
    printf("6. print chicken\n");
    printf("> ");
}


int main()
{
    Life life;
    int select;
    init_binary();
    memset(&life, 0, sizeof(Life));

    printf("[poultry-farm]\n");

    while (1) {
        menu();
        scanf("%d", &select);
        switch (select) {
            case 1:
            create_egg(&life);
            break;

            case 2:
            rename_egg(&life);
            break;

            case 3:
            print_egg(&life);
            break;

            case 4:
            observe_egg(&life);
            break;

            case 5:
            rename_chicken(&life);
            break;

            case 6:
            print_chicken(&life);
            break;

            case 7:
            printf("Bye!\n");
            exit(EXIT_SUCCESS);
            break;

            default:
            printf("Invalid Selection!\n");
        }
    }
}