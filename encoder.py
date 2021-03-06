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

def visit(statements):

    tokens = []
    
    for statement in statements:
    
        if isinstance(statement, Statement):
            tokens += statement.visit()
        else:
            tokens.append(str(statement))
    
    return tokens

class Tokens:

    def __init__(self):
        pass
    
    def __str__(self):
        return ""

class NewLine(Tokens):
    pass

class Print(Tokens):

    def __init__(self, *expressions):
        self.expressions = expressions
    
    def visit(self):
        return str(self)
    
    def __str__(self):
        if self.expressions:
            return "\xf1" + "".join(map(str, self.expressions))
        else:
            return "\xf1"

class Assign(Tokens):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
    
    def __str__(self):
        return str(self.name) + "=" + str(self.expression)

class UnaryOp(Tokens):

    def __init__(self, right):
        self.right = right
    
    def __str__(self):
        return self.token + str(self.right)

class NOT(UnaryOp):
    token = "\xac"


class BinaryOp(Tokens):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return str(self.left) + self.operator + str(self.right)

class Add(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "+", right)

class Subtract(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "-", right)

class Multiply(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "*", right)

class Divide(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "/", right)

class Equals(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "=", right)

class NotEquals(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "<>", right)

class LessThan(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "<", right)

class LessThanEquals(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "<=", right)

class GreaterThan(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, ">", right)

class GreaterThanEquals(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, ">=", right)

class DIV(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "\x81", right)

class MOD(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "\x83", right)

class AND(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "\x80", right)

class EOR(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "\x82", right)

class OR(BinaryOp):

    def __init__(self, left, right):
        BinaryOp.__init__(self, left, "\x84", right)


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


class VDU(Tokens):

    def __init__(self, arguments):
        self.arguments = arguments
    
    def __str__(self):
    
        return "\xef" + ",".join(map(str, self.arguments))


class Parens(Tokens):

    def __init__(self, expression):
        self.expression = expression
    
    def __str__(self):
        return "(" + str(self.expression) + ")"


class Byte(Parens):

    def __str__(self):
        return "?" + str(self.expression)

class Word(Parens):

    def __str__(self):
        return "!" + str(self.expression)


class Simple(Tokens):

    def __str__(self):
        return chr(self.value)


class Constant(Simple):
    pass

class FALSE(Constant):
    value = 0xa3

class TRUE(Constant):
    value = 0xb9

class RUN(Simple):
    value = 0xf9


class SystemVariable(Simple):
    pass

class PAGE(SystemVariable):
    value = 0x90

class TOP(SystemVariable):
    value = 0xb8

class LOMEM(SystemVariable):
    value =0xd2

class HIMEM(SystemVariable):
    value = 0xd3


class Tab(Tokens):

    def __init__(self, x, y = None):
        self.x = x
        self.y = y
    
    def __str__(self):
    
        output = "\x8a" + str(self.x)
        if self.y != None:
            output += "," + str(self.y) + ")"
        
        return output

class Cls(Tokens):

    def __str__(self):
        return "\xdb"

class End(Tokens):

    def __str__(self):
        return "\xe0"

class Proc(Tokens):

    def __init__(self, name, *arguments):
    
        self.name = name
        self.arguments = arguments
    
    def __str__(self):
    
        output = "\xf2" + self.name
        
        if self.arguments:
            output += "(" + ",".join(map(str, self.arguments)) + ")"
        
        return output

class Fn(Tokens):

    def __init__(self, name, *arguments):
    
        self.name = name
        self.arguments = arguments
    
    def __str__(self):
    
        output = "\xa4" + self.name
        
        if self.arguments:
            output += "(" + ",".join(map(str, self.arguments)) + ")"
        
        return output

class Call(Tokens):

    def __str__(self):
        return "\xd6"

class Builtin(Tokens):

    """Describes built-in functions and commands, defining their detokenised
    text and the tokens used to encode them.
    
    If a token needs to be encoded with parentheses, an opening parenthesis is
    stored after the token in the token attribute."""
    
    def __init__(self, *arguments):
    
        self.arguments = arguments
    
    def __str__(self):
    
        output = self.token + ",".join(map(str, self.arguments))
        if self.name.endswith("(") or self.token.endswith("("):
            output += ")"
        
        return output

class SIN(Builtin):
    name = "SIN("
    token = "\xb5"

class COS(Builtin):
    name = "COS("
    token = "\x9b"

class LEFT(Builtin):
    name = "LEFT$("
    token = "\xc0"

class MID(Builtin):
    name = "MID$("
    token = "\xc1"

class RIGHT(Builtin):
    name = "RIGHT$("
    token = "\xc2"

class MODE(Builtin):
    name = "MODE"
    token = "\xeb"

class RND(Builtin):
    name = "RND"
    token = "\xb3"
    
    def __str__(self):
    
        output = self.token
        if self.arguments:
            output += "(" + ",".join(map(str, self.arguments)) + ")"
        
        return output


class Statement:
    pass

class If(Statement):

    def __init__(self, test, then, else_ = None):
    
        self.test = test
        self.then = then
    
    def visit(self):
    
        tokens = ["\xe7" + str(self.test)]
        
        then_tokens = visit(self.then)
        
        # Join the IF token with the first THEN token but do not include a THEN
        # token (0x8c).
        tokens[0] += " " + then_tokens.pop(0)
        
        return tokens + then_tokens

class IfThenElse(Statement):

    def __init__(self, test, then, else_ = None):
    
        self.test = test
        self.then = then
        self.else_ = else_
    
    def visit(self):
    
        tokens = ["\xe7" + str(self.test)]
        
        then_tokens = visit(self.then)
        
        if self.else_:
            else_tokens = visit(self.else_)
            # Join the last token in the THEN list with the first in the ELSE
            # list.
            then_tokens[-1] += "\x8b" + else_tokens.pop(0)
        else:
            else_tokens = []
        
        # Join the IF token with the first THEN token, which may include the
        # first ELSE token.
        tokens[0] += "\x8c" + then_tokens.pop(0)
        
        return tokens + then_tokens + else_tokens

class ForNext(Statement):

    def __init__(self, assignment, limit, body, step = None):
    
        self.assignment = assignment
        self.limit = limit
        self.body = body
        self.step = step
    
    def visit(self):
    
        output = "\xe3" + str(self.assignment) + "\xb8" + str(self.limit)
        if self.step:
            output += "\x88" + str(self.step)
        
        tokens = [output, str(NewLine())]
        body_tokens = visit(self.body) + [str(NewLine()), "\xed"]
        return tokens + body_tokens

class RepeatUntil(Statement):

    def __init__(self, body, condition):
    
        self.body = body
        self.condition = condition
    
    def visit(self):
    
        tokens = ["\xf5", str(NewLine())]
        body_tokens = visit(self.body)
        condition_tokens = ["\xfd " + str(self.condition)]
        return tokens + body_tokens + condition_tokens

class DefProc(Statement):

    def __init__(self, name, arguments, body):
    
        self.name = name
        self.arguments = arguments
        self.body = body
    
    def visit(self):
    
        # Always start a definition on a new line.
        tokens = [str(NewLine())]
        tokens.append("\xdd\xf2" + self.name)
        
        if self.arguments:
            tokens[1] += "(" + ",".join(map(str, self.arguments)) + ")"
        
        tokens += visit(self.body)
        return tokens + ["\xe1"]

class DefFn(Statement):

    def __init__(self, name, arguments, body):
    
        self.name = name
        self.arguments = arguments
        self.body = body
    
    def visit(self):
    
        # Always start a definition on a new line.
        tokens = [str(NewLine())]
        tokens.append("\xdd\xa4" + self.name)
        
        if self.arguments:
            tokens[1] += "(" + ",".join(map(str, self.arguments)) + ")"
        
        tokens += visit(self.body)
        return tokens

class Return(Statement):

    def __init__(self, expression):
    
        self.expression = expression
    
    def visit(self):
    
        tokens = ["=" + str(self.expression)]
        return tokens

class Dim(Statement):

    def __init__(self, name, expression):
    
        self.name = name
        self.expression = expression
    
    def visit(self):
    
        tokens = ["\xde" + name + "(" + str(self.expression) + ")"]
        return tokens


class Encoder:

    def __init__(self):
    
        pass
    
    def encode(self, statements, start = 10, step = 10):
    
        tokens = visit(statements)
        
        output = []
        n = start
        length = 4
        current = ""
        
        for token in tokens:
        
            if token == "":
                output.append("\r" + struct.pack(">HB", n, length - 1) + current[:-1])
                length = 4
                current= ""
                n += step
                continue
            
            new_length = length + len(token) + 1
            
            if length > 255:
                # Write the current line and start a new one for the statement.
                output.append("\r" + struct.pack(">HB", n, length - 1) + current[:-1])
                length = 4
                n += step
            
            current += token + ":"
            length = new_length
        
        if length > 4:
            output.append("\r" + struct.pack(">HB", n, length - 1) + current[:-1])
        
        output += "\r\xff"
        return "".join(output)
