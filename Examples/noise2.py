#!/usr/bin/env python

import builder
from encoder import *

"""
MODE5
VDU23,1,0;0;0;0;
A%=&18
REPEAT
!(&3000+RND(&4FFF))=RND
?&FE03=A%
A%=A%+1
IF A%=&40 A%=&18
UNTIL FALSE
"""

enc = Encoder()

listing = [
    MODE(5), NewLine(),
    VDU([23, 1, "0;0;0;0;"]), NewLine(),
    Assign("A%", "&18"), NewLine(),
    RepeatUntil([
        Assign(Word(Parens(Add("&3000", RND("&4FFF")))), RND()), NewLine(),
        Assign(Byte("&FE03"), "A%"), NewLine(),
        Assign("A%", Add("A%", 1)), NewLine(),
        IfThenElse(Equals("A%", "&40"), [Assign("A%", "&18")]), NewLine()
        ], FALSE()), NewLine()
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
