//gcc chal.c -o chal
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <signal.h>
#include <time.h>


#define BOXER 1
#define YELLOW 2
#define YELLOW_WIN "22222"

typedef struct {
  char name[16];
  long HP;
  long type;
  void (*build)(void *);
  void (*destroyed)(void *);
} Bunker;

typedef struct {
  char name[16];
  long HP;
  long type;
  void (*build)();
  void (*destroyed)();
} Hatchery;

void proc_init ()
{
  setvbuf (stdin, 0, 2, 0);
  setvbuf (stdout, 0, 2, 0);
  setvbuf (stderr, 0, 2, 0);
}

int read_input (char *buf, int len)
{
  int ret;

  ret = read (0, buf, len);

  if (ret < 0)
  {
    fprintf (stderr, "read error!\n");
    exit (1);
  }

  if (buf[ret-1] == '\n')
    buf[ret-1] = '\0';

  return ret;
}


int read_number ()
{
  char buf[16];
  int ret;
  int number;

  ret = scanf (" %d", &number);

  return number;
}

void buildHatchery(Hatchery* this)
{
  puts("Your drone is transformed to Hatchery");
}

void destroyedHatchery(Hatchery* this)
{
  puts("Hatchery is destructed...");
}

Hatchery* newHatchery(long hp) 
{
  Hatchery* hatchery = (Hatchery*)malloc(sizeof(Hatchery));

  strcpy(hatchery->name, "Hatchery");
  hatchery->build = buildHatchery;
  hatchery->destroyed = destroyedHatchery;
  //Boxer changed this line to comment.
  //hatchery->type = YELLOW;
  hatchery->HP = hp;

  return hatchery;
}

void buildBunker(Bunker* this)
{
  puts("SCV starts to build a bunker");
}

void destroyedBunker(Bunker* this)
{
  puts("Bunker is destructed...");
  if(this->type && !strcmp ((char*)(this->type), YELLOW_WIN))
    system("cat flag");
}

Bunker* newBunker(long hp) 
{
  Bunker* bunker = (Bunker*)malloc(sizeof(Bunker));

  strcpy(bunker->name, "Bunker");
  bunker->build = buildBunker;
  bunker->destroyed = destroyedBunker;
  //Yellow changed this line to comment.
  //bunker->type = BOXER;
  bunker->HP = hp;

  return bunker;
}

char canwin='N';
void BuildHatchery() 
{
  puts ("your drone moved to outside.");

  Hatchery* hatchery = newHatchery(0x1250);
  hatchery->build(hatchery);
  Bunker* bunker = newBunker(0x350);
  bunker->build(bunker);

  puts("your drone came out and attacked bunker!");
  puts("now can you beat BoxeR? [y/N]");
  scanf(" %c", &canwin);

  if((char)canwin != 'N') {
    puts("Drones finally destroyed the bunker!");
    bunker->destroyed(bunker);
    puts("Mission Success");
    bunker = NULL;
  } else {
    puts("Bunker is completed");
    hatchery->destroyed(hatchery);
    puts("Failed to mission");
    hatchery = NULL;
  }

  sleep(1);
  exit(0);
}

#define DEFAULT_SIZE 1024
char * buffer = 0;
long size = 0;
void BunkerRushStudy () 
{
  int ret;
  unsigned course;

  printf("your buffer: %p\n", buffer);
  puts("Select your course");
  printf(">> ");
  course = read_number();


  if (course > 2) {
    return;
  }

  if (course < 2) {
    if (buffer == NULL) {
      buffer = (char*)malloc(DEFAULT_SIZE);
      size = DEFAULT_SIZE;
    }
    ret = setvbuf(stdin, buffer, course, size);
  } else {
    ret = setvbuf(stdin, 0, course, 0);
  }

  if (ret < 0) {
    puts("study fail...");
    exit(1);
  }
  puts("Finish and sleep.");  
}

void BuildSpawningPool() {
  
  printf("buffer: ");
  scanf("%lu", &buffer);
  printf("size: ");
  scanf("%lu", &size);

  if (size >0x10000)
    size = 0;
}
void print_menu ()
{
  puts("1. Build Hatchery");
  puts("2. Study Bunkering");
  printf(">> ");
}


int main ()
{
  proc_init(); 
  puts("======================================");
  puts("    Mission: build another Hatchery   ");
  puts("======================================");

  while (1) {
    int menu;
    print_menu();
    menu = read_number();

    switch (menu) {
      case 1:
        BuildHatchery();
        break;

      case 2:
        BunkerRushStudy();
        break;

      case 0x22222:
        BuildSpawningPool();
        break;
        
      default:
        break;
    }
  }
}
