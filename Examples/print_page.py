#!/usr/bin/env python

import builder
from encoder import *

enc = Encoder()

listing = [
    Print(PAGE()),
    Print("~", PAGE())
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
