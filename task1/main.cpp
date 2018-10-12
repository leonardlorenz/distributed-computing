#include <iostream>
#include <unistd.h>
#include <sys/param.h>

/**
 * char name[]:
 *      a character array that stores the hostname
 * int MAXHOSTNAMELEN:
 *      constant provided by param.h, size of the hostname char[]
 * int gethostname(char[] hostname, sizeof hostname):
 *      writes the hostname to the char[] that gets parsed over
 **/
int main(int argc, char** argv){
    char name[MAXHOSTNAMELEN];
    gethostname(name, sizeof name);
    std::cout << name << std::endl;
}
