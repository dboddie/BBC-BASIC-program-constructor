#!/usr/bin/env python

import builder
from encoder import *

"""
MODE 5
!&C00=&10204080:!&C04=&01020408
!&C08=&08040201:!&C0C=&80402010
REPEAT
VDU 223+RND(2)
UNTIL FALSE
"""

enc = Encoder()

listing = [
    MODE(5), NewLine(),
    Assign("!&C00", "&10204080"), NewLine(),
    Assign("!&C04", "&01020408"), NewLine(),
    Assign("!&C08", "&08040201"), NewLine(),
    Assign("!&C0C", "&80402010"), NewLine(),
    RepeatUntil([VDU([Add(223, RND(2))]), NewLine()],
        FALSE())
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
