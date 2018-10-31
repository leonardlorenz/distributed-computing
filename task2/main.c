#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include<arpa/inet.h>

void error(const char *msg){
    perror(msg);
    exit(0);
}

void host_name_to_ip(char* ip, struct hostent *host_name){
	struct in_addr **addr_list;
	addr_list = (struct in_addr **) host_name->h_addr_list;

    /** gather ip and copy it to the ip variable **/
	int i;
	for(i = 0; addr_list[i] != NULL; i++) {
		strcpy(ip , inet_ntoa(*addr_list[i]));
	}
    /** concatenate ip with newline char **/
    char* output_str;
    strcat(output_str, ip);
    strcat(output_str, "\n");
    printf(output_str);
}

int main(int argc, char** argv){
    /** init launch parameter variables **/
    struct hostent* server = gethostbyname("dbl44.beuth-hochschule.de");
    char ip[20];
    host_name_to_ip(ip, server);
    int portno = 44444;

    printf("initialized launch parameters\n");

    /** init socket **/
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        error("ERROR opening socket");
    }

    printf("initialized socket\n");

    /** init connection **/
    struct sockaddr_in serv_addr;
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(portno);

    printf("initialized connection parameters\n");

    socklen_t addrlen;
    addrlen = sizeof(serv_addr);

    int connection;
    if(connection = connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0){
        error("connection failed");
    } else {
        printf("connected\n");
    }

    /** create string to send over connection **/
    int buffer_size;
    char* buffer[1024];
    buffer_size = sizeof(buffer);

    /** clear buffer with zeros and write packet string to it **/
    memset(&buffer, '0', buffer_size);
    strcpy((char*) buffer, "dslp/1.0\r\nrequest time\r\ndslp/end");

    printf("string ready\n");

    /** write buffer to socket **/
    if(send(sockfd, buffer, buffer_size, 0) < 0){
        printf("packet sending failed");
    } else {
        printf("packet sent\n");
    }

    /** clear buffer, then read answer **/
    bzero((char*) buffer, buffer_size);
    recv(sockfd, buffer, buffer_size, 0);

    printf("packet received\n");

    printf("%d\n", read);
    printf("%s\n", buffer);

    printf("done");
}
