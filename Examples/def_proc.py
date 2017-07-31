#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Proc("x"),
    End(),
    DefProc("x", [], [
        Print('"Hello world!"')
        ])
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
