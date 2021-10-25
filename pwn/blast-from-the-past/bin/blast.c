#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	
//	sleep(3);

	FILE *fp;
	unsigned char inp;
	fp = fopen("/dev/urandom", "r");
	fread(&inp, 1, 1, fp);
	fclose(fp);

//	make stack space to avoid guessing offsets
//	printf("Byte is: %hhx\n", inp);
	char lol[inp * 3];
	lol[inp-2] = inp;
	alloca(16 * inp / 30);

	printf("welcome home, %p\n", printf);
	printf("enter password: ");
	fgets(lol, inp * 3, stdin);
	printf(lol);
	_exit(0);

}
