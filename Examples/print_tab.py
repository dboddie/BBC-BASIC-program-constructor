#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Cls(),
    ForNext(Assign("Y%", 1), 23, [
        ForNext(Assign("X%", 1), 39, [
            Print(Tab("X%", "Y%"), ';"*";')
            ], step = 2)
        ], step = 2)
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
