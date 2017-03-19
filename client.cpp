/*
** client.c -- a stream socket client demo
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <iostream>
#include <fstream>

#include <arpa/inet.h>



#define HOST  "127.0.0.1"
#define PORT  10000

using namespace std;
int sockfd;
struct sockaddr_in serv_addr;


// trimit catre serv dim octeti ce se afla in vectorul info
// si returnez numarul de octeti cititi
int sendInfo(int serv, char * info, int dim)
{
	char c, *buffer;
	buffer = info;
	int i;
	for ( i = 0 ; i < (int) dim ; i++)
	{
		c = *buffer;
		int sent = send(serv, &c, 1, 0 );
		if (sent < 0 )
			return -1;
		if (sent == 0)
		{
			cout << "sendInfo primesc 0 de ce??????\n\n\n";
		}
		buffer++;
	}
	return i;
}

int main(int argc, char *argv[])
{
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0)
		perror("ERROR opening socket");
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	inet_aton(HOST, &serv_addr.sin_addr);

	if (connect(sockfd, (struct sockaddr*) &serv_addr, sizeof(serv_addr)) < 0)
		perror("ERROR connecting");

	char a[500] = "Segfault Tigers";
	sendInfo(sockfd, a, strlen(a) + 1);
	//cin.getline(a,100);
	cout<<"asdadasdasd\n\n\n\n";
	srand(time(NULL));
	while (1)
	{
		char q[5];
		unsigned short int x;//  = rand() % 640;
		unsigned short int y;//  = rand() % 480;
		char  press;//  = rand() % 2;
		int z;
		cout<<"before read\n";
		cin >> x >> y >> z;
		press = z;
		cout<<"after read\n";
		cout << "comenzi\n";
		cout << x << " " << " " << y << " " << press << '\n';
		cout.flush();
		q[0] = x >> 8;
		q[1] = x & 0xff;
		q[2] = y >> 8;
		q[3] = y & 0xff;
		q[4] = press;
		sendInfo(sockfd, q, 5);

	}

	return 0;
}