#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Assign("A%", 0), NewLine(),
    Print("A%"),
    Assign("A%", BinaryOp("A%", "+", 1)),
    IfThenElse(BinaryOp("A%", "<", 10), [Goto(20)])
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
