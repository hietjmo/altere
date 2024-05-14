

import subprocess
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('basename', nargs='?', default="program")
  pad ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

def execute (command,success="Done."):
  try:
    subprocess.run(command, check=True)
    print (success)
  except subprocess.CalledProcessError as e:
    print ("Error:", e)
    return 0
  return 1

assembly_code = r"""
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
"""

asm_file = args.basename + ".asm"
obj_file = args.basename + ".o"
output_file = args.basename

with open(asm_file, 'w') as f:
  f.write (assembly_code)
print (f"Wrote assembly code to: {asm_file}")
command1 = ["as", "-o", obj_file, asm_file]
success1 = "Assembly code assembled successfully."
command2 = ["ld", "-o", output_file, obj_file]
success2 = "Object file linked successfully."

if execute (command=command1,success=success1) and execute (command=command2,success=success2):
  print (f"Wrote executable to: {output_file}")

# as -o hello.o hello.asm
# ld -o hello hello.o
# ./hello

