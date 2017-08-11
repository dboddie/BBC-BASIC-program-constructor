#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Print('"x=";', 123),
    Print('"x*x=";', Fn("a", 123)),
    End(),
    DefFn("a", ["X"], [
        Return(Multiply("X", "X"))
        ])
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
