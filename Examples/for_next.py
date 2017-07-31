#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    [ForNext(BinaryOp("A%", "=", 1), 11, Print("A%"), step = 2)]
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
