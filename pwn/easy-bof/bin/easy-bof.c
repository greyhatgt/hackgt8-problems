#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include "easy-bof.h"

int main() {
	int DAYS_SINCE_LAST_INTRUSION_ATTEMPT = 1;
	int access_granted = 0;
	char super_secret_input[1024];
	puts("You have entered the secret lair of the Bank of America.");
	puts("What is the password?");

	read(0, super_secret_input, BUF_SIZE);
	if (access_granted) {
		puts("Didn't think you had it in you. Welcome to the club.");
		system("/bin/sh");
	} else {
		DAYS_SINCE_LAST_INTRUSION_ATTEMPT++;
		puts("Ha, try again next time.");
	}
	return 1;
}
	
