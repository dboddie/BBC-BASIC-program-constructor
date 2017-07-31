"""
Copyright (C) 2017 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import struct

class Tokens:

    def __init__(self):
        pass

class Print(Tokens):

    def __init__(self, *args):
        self.values = args
    
    def __str__(self):
        if self.values:
            return "\xf1" + "".join(map(str, self.values))
        else:
            return "\xf1"

class Assign(Tokens):

    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return str(self.name) + "=" + str(self.value)

class BinaryOp(Tokens):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return str(self.left) + self.operator + str(self.right)

class Goto(Tokens):

    def __init__(self, number):
        self.number = number
    
    def __str__(self):
        if self.number < 32768:
            d0 = self.number % 64
            d1 = (self.number / 64) % 4
            d2 = ((self.number / 64) / 4) % 64
            d3 = (((self.number / 64) / 4) / 64) % 2
            a = 0x54 ^ (d1 << 4) ^ (d3 << 2)
            b = 0x40 + d0
            c = 0x40 + d2
            return "\xe5\x8d" + struct.pack("<BBB", a, b, c)
        else:
            return "\xe5\x8d" + str(self.number)

class PAGE(Tokens):

    def __str__(self):
        return "\x90"

class IfThenElse(Tokens):

    def __init__(self, test, then, else_ = None):
    
        self.test = test
        self.then = then
        self.else_ = else_
    
    def __str__(self):
    
        output = "\xe7" + str(self.test) + "\x8c" + str(self.then)
        if self.else_:
            output += "\x8b" + str(self.else_)
        
        return output

class ForNext(Tokens):

    def __init__(self, assignment, limit, body, step = None):
    
        self.assignment = assignment
        self.limit = limit
        self.body = body
        self.step = step
    
    def __str__(self):
    
        output = "\xe3" + str(self.assignment) + "\xb8" + str(self.limit)
        if self.step:
            output += "\x88" + str(self.step)
        
        output += ":" + str(self.body)
        output += ":" + "\xed"
        return output


class Encoder:

    def __init__(self):
    
        pass
    
    def encode(self, lines, start = 10, step = 10):
    
        output = []
        n = start
        
        for line in lines:
        
            statements = self.statements(line)
            line_data = ":".join(statements)
            output.append("\r" + struct.pack(">HB", n, len(line_data) + 4) + line_data)
            n += step
        
        output += "\r\xff"
        return "".join(output)
    
    def statements(self, line):
    
        output = []
        
        for statement in line:
            output.append(str(statement))
        
        return output
