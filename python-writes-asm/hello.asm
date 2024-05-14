
.data
    hello_msg: .ascii "Hello, World!\n"

.text
.global _start

_start:
    # write the message to stdout
    mov     $4, %eax        # syscall number for sys_write
    mov     $1, %ebx        # file descriptor 1 (stdout)
    mov     $hello_msg, %ecx   # address of the message
    mov     $14, %edx       # length of the message
    int     $0x80           # call kernel

    # exit the program
    mov     $1, %eax        # syscall number for sys_exit
    xor     %ebx, %ebx      # exit code 0
    int     $0x80           # call kernel
