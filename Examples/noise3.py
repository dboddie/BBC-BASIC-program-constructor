#!/usr/bin/env python

import builder
from encoder import *

"""
MODE2
?&FE00=0
M%=2
A%=&18
B%=0
REPEAT
!(&3000+RND(&4FFF))=RND
?&FE03=A%
A%=A%+1
IF A%=&40 A%=&18
B%=B%+1
IF B%=256 B%=0:M%=M%+1:?&FE07=(M%AND7)*8
UNTIL FALSE
"""

enc = Encoder()

listing = [
    MODE(2), NewLine(),
    Assign(Byte("&FE00"), 0), NewLine(),
    Assign("M%", 2), NewLine(),
    Assign("A%", "&18"), NewLine(),
    Assign("B%", 0), NewLine(),
    RepeatUntil([
        Assign(Word(Parens(Add("&3000", RND("&4FFF")))), RND()), NewLine(),
        Assign(Byte("&FE03"), "A%"), NewLine(),
        Assign("A%", Add("A%", 1)), NewLine(),
        IfThenElse(Equals("A%", "&40"), [Assign("A%", "&18")]), NewLine(),
        Assign("B%", Add("B%", 1)), NewLine(),
        If(Equals("B%", 256), [
            Assign("B%", 0), Assign("M%", Add("M%", 1)),
            Assign(Byte("&FE07"), Multiply(Parens(AND("M%", 7)), 8))
            ]), NewLine()
        ], FALSE()), NewLine()
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
