#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char item[1024];

void sell() {
	puts("Sorry, we are out of that item!");
}

void update() {
	char buf[1024];
	printf("Enter new item name: ");
	gets(buf);
	memcpy(buf, item, 1024);
}

void close_store() {
	puts("Closing the store today. Goodbye!");
	exit(0);
}

void help() {
	printf(
		"(s)ell:\t\tsell your item\n"
		"(u)pdate:\tupdate currently available item\n"
		"(c)lose:\tclose the store\n"
		"(h)elp:\t\tprint this message again\n"
	);
}

void loop() {
	char inp;
	for (;;) {
		printf("Enter action: ");
		inp = getchar();
		getchar();
		switch(inp) {
			case 's':
				sell();
				break;
			case 'u':
				update();
				break;
			case 'c':
				close_store();
				break;
			default:
				puts("Unrecognized command.");
			case 'h':
				help();
				break;
		}
	}
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
        setvbuf(stdin, NULL, _IONBF, 0);
	help();
	loop();
}
