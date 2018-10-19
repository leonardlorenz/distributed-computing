#include <sys/socket.h>
#include <sys/types.h>
#include <string.h>
#include <netinet/in.h>
#include <netdb.h>
#include <cstdio>
#include <unistd.h>

int main(int argc, char** argv){
    struct sockaddr_in serv_addr;
    struct hostent *server;

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    server = gethostbyname("dbl44.beuth-hochschule.de");
    int portno = 44444;

    int n;

    char buffer[256];

    /** clear the server address **/
    bzero((char *) &serv_addr, sizeof(serv_addr));

    /** set connection protocol for remote address **/
    serv_addr.sin_family = AF_INET;

    /** copy server adress to host struct **/
    bcopy((char *)server->h_addr,
        (char *)&serv_addr.sin_addr.s_addr,
        server->h_length);

    /** set host struct port number **/
    serv_addr.sin_port = htons(portno);

    /** connect to the host server **/
    int connection = connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr));

    /** clear the packet buffer **/
    bzero(buffer,256);

    /**
     * TODO
     * 1. write to the buffer as a byte array
     * 2. write the timecode packet
     */

    /** read out the buffer we created **/
    fgets(buffer, 255, stdin);

    /** write the stream to the socket **/
    n = write(sockfd, buffer, strlen(buffer));

    /**
     * TODO
     * 1. read out the package sent by the server
     * 2. display it in the terminal
     */

    /** clear the buffer again **/
    bzero(buffer, 256);

    /** read the answer from host **/
    n = read(sockfd, buffer, 255);
    return 0;
}
