#!/usr/bin/env python

import builder
from encoder import *

"""
MODE 5
VDU 23,224,128,64,32,16,8,4,2,1
VDU 23,225,1,2,4,8,16,32,64,128
REPEAT
VDU 223+RND(2)
A%=RND(4)-1
B%=A%+2 MOD 4
A%=&C00+A%*4
B%=&C00+B%*4
!A%=!A% EOR !B%
UNTIL FALSE
"""

enc = Encoder()

listing = [
    MODE(5), NewLine(),
    VDU([23,224,128,64,32,16,8,4,2,1]), NewLine(),
    VDU([23,225,1,2,4,8,16,32,64,128]), NewLine(),
    RepeatUntil([
        VDU([Add(223, RND(2))]), NewLine(),
        Assign("A%", Subtract(RND(4), 1)), NewLine(),
        Assign("B%", MOD(Parens(Add("A%", 2)), 4)), NewLine(),
        Assign("A%", Add("&C00", Parens(Multiply("A%", 4)))), NewLine(),
        Assign("B%", Add("&C00", Parens(Multiply("B%", 4)))), NewLine(),
        Assign("!A%", EOR("!A%", "!B%")), NewLine()
        ],
        FALSE())
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
