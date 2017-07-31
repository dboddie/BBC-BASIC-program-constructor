#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Proc("x", 10),
    End(),
    DefProc("x", ["a%"], [
        ForNext(Assign("i%", 1), "a%", [
            Print('i%;" out of ";a%')
            ])
        ])
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
