#!/usr/bin/env python

import builder
from encoder import *

"""
MODE 7
C%=0
REPEAT
IF C%=0 THEN VDU 145:C%=1
A%=RND(2)
VDU 154+(A%*15),290-(A%*62)
C%=C%+2
IF C%=39 THEN PRINT:C%=0
UNTIL FALSE
"""

enc = Encoder()

listing = [
    MODE(7), NewLine(),
    Assign("C%", 0), NewLine(),
    RepeatUntil([
        IfThenElse(Equals("C%", 0), [
            VDU([145]),
            Assign("C%", 1)
            ]), NewLine(),
        Assign("A%", RND(2)), NewLine(),
        VDU([Add(154, Parens(Multiply("A%", 15))),
             Subtract(290, Parens(Multiply("A%", 62)))]), NewLine(),
        Assign("C%", Add("C%", 2)), NewLine(),
        IfThenElse(Equals("C%", 39), [
            Print(), Assign("C%", 0)
            ]), NewLine()
        ],
        FALSE())
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
