#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Assign("A%", 0),
    RepeatUntil(
        [Assign("B%", Multiply("A%", 2)),
         Print('A%;" ";B%'),
         Assign("A%", Add("A%", 1))],
        Equals("A%", 10))
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
