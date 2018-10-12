#include <iostream>
#include <unistd.h>
#include <sys/param.h>

int main(int argc, char** argv){
    char name[MAXHOSTNAMELEN];
    gethostname(name, sizeof name);
    std::cout << name << std::endl;
}
