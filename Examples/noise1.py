#!/usr/bin/env python

import builder
from encoder import *

"""
FOR A%=8 TO &20
?&FE03=A%
!(&1000+(RND AND &7FFF))=RND
NEXT
RUN
"""

enc = Encoder()

listing = [
    ForNext(BinaryOp("A%", "=", 8), "&20", [
        Assign("?&FE03", "A%"),
        Assign(Word(Parens(Add("&1000", Parens(AND(RND(), "&7FFF"))))), RND())
        ]), NewLine(),
        RUN(), NewLine()
    ]

program = enc.encode(listing, start = 10, step = 10)

files = [("CODE", 0xe00, 0xe00, program)]

builder.build(files)
