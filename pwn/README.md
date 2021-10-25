### Author: Ptomerty

## Easy Bof

This program has a buffer overflow, since BUF_SIZE is misdefined in `easy-bof.h`. Thus, if we input more characters than the buffer size, we will overflow the buffer into the `access_granted` variable and get a shell. For more reading: https://en.wikipedia.org/wiki/Buffer_overflow

## Market Maaking

The intended solution was to use the gets() overflow in update() to construct a ropchain. A sample exploit would look like this:
- redirect execution to call puts(puts@GOT) with a `pop rdi; ret` gadget
- with this libc leak, identify libc version through libc-database and calculate offsets to other system functions
- redirect to gets() again somehow. Either use a stack pivot to .bss or just construct a ropchain consisting of system("/bin/sh").
Win!

## Blast from the Past

Unsolved during HackGT...give it a go!