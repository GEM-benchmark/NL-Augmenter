#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grammaire
Copyright 2021-present NAVER Corp.
Created on Wed Jul 21 10:40:14 2021

@author: claude.roux@naverlabs.com
@author: caroline.brun@naverlabs.com
"""

import re
# import tokenize
# from io import BytesIO


# ------------------------------------------------------------------------------
# Compiling the rules
# ------------------------------------------------------------------------------
# The rules are transformed into an automaton, where each rule element
# is a ssociated with a Python function that will be executed on the current
# token, according to the rule element definition (see evalRuleElement)
# Each element is evaluated to detect, which function to call: functioncode.
#
# Rule:
#
#    LABEL = element element ... element
# Important: the '=' must be enclosed with spaces
#
# Rule Element is:                                   Function
#   ?: any token                                    [anytoken]
#   ?*: any token zero or more                      [anystar]
#   ?+: any token one or more                       [anyplus]
#   "x" : character x                               [regularone]
#   "x"* : character x zero or more                 [tokenstarone]
#   "x"+ : character x one or more                  [tokenplusone]
#   token: any token                                [regularone]
#   token|token|token: defines list of tokens       [regular]
#   %rgx: rgx is then a regular expression          [tokenrgx]
#   !call: a capsule, call is: def call(token):...  [capsule]
#   str(xx)uu: an optional part within a string     [regular]
#   (str): an optional string                       [optionalone]
#   (str|str): an optional string list              [optional]
#   (%rgx): an optional regular expression          [optionalrgx]
#   (!call): an optional capsule                    [optionalcapsule]
#   token* : zero or more token                     [tokenstarone]
#   token+ : one or more token                      [tokenplusone]
#   [token|token|token]* : zero or more in list     [tokenstar]
#   [token|token|token]+ : one or more in list      [tokenplus]
#   [rgx]* : zero or more regular expression        [tokenrgxstar]
#   [rgx]+ : one or more regular expression         [tokenrgxplus]
#   [!call]* : zero or more capsule application     [capsulestar]
#   [!call]+ : one or more capsule application      [capsuleplus]
#   <element> : mark an element for a variable in head %x
#   <element>+ : mark an element for a variable in head %x
#   <element>* : mark an element for a variable in head %x
# ------------------------------------------------------------------------------
# Capsule function:
# A capsule function takes as arguments:
#  1) the list of tokens (tokens)
#  2) the position of the current token (pos)
#  3) the next rule element (rnxt)
# Example: def mycapsule(tokens, pos, rnxt): ...
# ------------------------------------------------------------------------------
# Variables
# You can mark an element for a variable, which is used in the rule head
# discover %1 = find <%\w+>+ out
# I find his secret out ---> i discover his secret
# <%\w+>+ is associated to %1
# For each marked element, there should be a variable %n on the left side
# ------------------------------------------------------------------------------
# This the way you can raise exception in Python
# ------------------------------------------------------------------------------
class GrammarError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return self.message.format(self.expression)


# ------------------------------------------------------------------------------
# evalRuleElement evaluates a rule element to detect its matching function
# ------------------------------------------------------------------------------
def erreur(w, err):
    err = GrammarError(w, err + ": '" + w + "'")
    raise err

pipeInsideCharacter = "÷…"

def checkpipe(w):
    # we need to check if a | is in a string
    ps = []
    opn = 1
    i = 0
    sz = len(w)
    while i < sz:
        c = w[i]
        if c == '"':
            opn = 1 - opn
        elif c == '|':
            if not opn:
                ps.append(i)
        i += 1
    if ps:
        ps.reverse()
        for i in ps:
            w = w[:i] + pipeInsideCharacter + w[i+1:]
    return w

def assess_any(w, functions, sz):
    if "|" in w:
        return assess_pipe(w, functions, sz)

    if sz == 1:
        function = anytoken
    elif sz > 2:
        erreur(w, "Unknown command")
    elif w[1] == '+':
        function = anyplus
    elif w[1] == '*':
        function = anystar
    return [function, w, True]


def assess_quote(w, functions, sz):
    if sz < 3:
        erreur(w, "Unknown quoted expression")
    if w[-1] == '"':
        w = w[1:-1]
        function = regularone
    elif w[-2] == '"':
        if w[-1] == '+':
            w = w[1:-2]
            function = tokenplusone
        elif w[-1] == '*':
            w = w[1:-2]
            function = tokenstarone
        else:
            erreur(w, "Unknown quoted expression")
    if pipeInsideCharacter in w:
        w = w.replace(pipeInsideCharacter, "|")
    return [function, w, True]


def assess_bracket(w, functions, sz):
    if sz < 3:
        erreur(w, "Unknown bracket expression")
    if w[-1] == ']':
        w = w[1:-1]
        return analyzeRuleElement(w, functions, 0)
    if w[-2] == ']':
        if w[-1] == '*':
            w = w[1:-2]
            return analyzeRuleElement(w, functions, 1)
        elif w[-1] == '+':
            w = w[1:-2]
            return analyzeRuleElement(w, functions, 2)
        else:
            erreur(w, "Unknown bracket expression")

def assess_skip(w, functions, sz):
    if sz < 3:
        erreur(w, "Unknown skip expression")
    if w[-1] == '>':
        w = w[1:-1]
        res = analyzeRuleElement(w, functions, 0)
    if w[-2] == '>':
        if w[-1] == '*':
            w = w[1:-2]
            res = analyzeRuleElement(w, functions, 1)
        elif w[-1] == '+':
            w = w[1:-2]
            res = analyzeRuleElement(w, functions, 2)
        else:
            erreur(w, "Unknown skip expression")
    res[-1] = False
    return res

def assess_rgx(w, functions, sz):
    if "|" in w:
        return assess_pipe(w, functions, sz)

    if sz == 1:
        erreur(w, "Incomplete regular expression")
    w = re.compile(w[1:])
    return [tokenrgx, w, True]


def assess_capsule(w, functions, sz):
    if "|" in w:
        return assess_pipe(w, functions, sz)

    if sz == 1:
        erreur(w, "Incomplete function name")
    w = functions[w[1:]]
    return [capsule, w, True]


def assess_pipe(w, functions, sz):
    elements = w.split("|")
    allregular = True
    w = []
    for e in elements:
        res = analyzeRuleElement(e, functions, 0)
        if res[0] != regularone:
            allregular = False
        w.append(res)
    if allregular:
        return [regular, elements, True]
    return [multiple, w, True]


def assess_optional(w, functions, sz):
    if sz < 3:
        erreur(w, "Unknown parenthetic expression")
    po = w.find('(')
    pf = w.find(')')
    if pf == -1:
        erreur(w, "missing closing parenthesis")
    sub = w[:po]
    if pf + 1 == sz:
        if po == 0:
            w = w[1:-1]
            return analyzeRuleElement(w, functions, 3)
        else:
            end = sub + w[po + 1:-1]
            w = [sub, end]
    else:
        end = w[pf + 1:]
        inter = w[po + 1:pf]
        w = [sub + end, sub + inter + end]
    return [regular, w, True]


def assess_all(w, functions, sz):
    if "(" in w:
        return assess_optional(w, functions, sz)
    if "|" in w:
        return assess_pipe(w, functions, sz)

    if w[-1] == '+':
        w = w[:-1]
        function = tokenplusone
    elif w[-1] == '*':
        w = w[:-1]
        function = tokenstarone
    else:
        function = regularone
    return [function, w, True]

def return_normal(function, w, skips):
    return [function, w, skips]

def return_star(function, w, skips):
    if function == multiple:
        function = multiplestar
    elif function == regularone:
        function = tokenstarone
    elif function == regular:
        function = tokenstar
    elif function == tokenrgx:
        function = tokenrgxstar
    elif function == capsule:
        function = capsulestar
    return [function, w, skips]


def return_plus(function, w, skips):
    if function == multiple:
        function = multipleplus
    elif function == regularone:
        function = tokenplusone
    elif function == regular:
        function = tokenplus
    elif function == tokenrgx:
        function = tokenrgxplus
    elif function == capsule:
        function = capsuleplus
    return [function, w, skips]


def return_optional(function, w, skips):
    if function == multiple:
        function = optionalmultiple
    elif function == regularone:
        function = optionalone
    elif function == regular:
        function = optional
    elif function == tokenrgx:
        function = optionalrgx
    elif function == capsule:
        function = optionalcapsule

    return [function, w, skips]



# If the first character is a key in selections, we call the matching function
assesses = {"?": assess_any, '"': assess_quote, '[': assess_bracket, '<': assess_skip, "%": assess_rgx, "!": assess_capsule}
on_brackets = {0: return_normal, 1: return_star, 2: return_plus, 3: return_optional}


# We analyse the rule element
def analyzeRuleElement(w, functions, brackets):
    if "|" in w and '"' in w:
        w = checkpipe(w)
    try:
        function, w, skips = assesses[w[0]](w, functions, len(w))
    except KeyError:
        function, w, skips = assess_all(w, functions, len(w))

    return on_brackets[brackets](function, w, skips)


# ------------------------------------------------------------------------------
# Rules are all indexed on their first elements
# ------------------------------------------------------------------------------
def indexonhead(automate, w, head, nb):
    idx = automate["_++_"]
    if w in idx:
        heads = idx[w]
        if not nb:
            heads.append(head)
            return
        found = -1
        # We sort out heads according to their rule length
        # We keep the longest in front
        for i in range(len(heads)):
            if nb > len(automate[heads[i]]):
                found = i
                break
        if found != -1:
            heads.insert(found, head)
        else:
            heads.append(head)
    else:
        idx[w] = [head]

def indexonheadrgx(automate, w, head):
    if w in automate:
        automate[w].append(head)
    else:
        automate[w] = [head]

# ------------------------------------------------------------------------------
# The compiler itself
# ------------------------------------------------------------------------------
def compiling(v, functions):
    v = [s.replace("\t", " ") for s in v if len(s) != 0]
    v = [s.strip().split(' ') for s in v if len(s) != 0]
    automate = {"_++_": {}}
    automate["_**_"] = {}
    for r in v:
        if r[0][0] == "#":
            continue
        head = ""
        foundequal = False
        initial = True
        rule = []
        r = [s for s in r if len(s) != 0]
        nb = len(r)
        for w in r:
            if not foundequal:
                nb -= 1
                if w == '=':
                    foundequal = True
                else:
                    if head != "":
                        head += " "
                    head += w
            else:
                e = analyzeRuleElement(w, functions, 0)
                if initial:
                    while head in automate:
                        head += "…∞"
                    initial = False
                    # These are the elements, on which we can index our rules
                    if e[0] == regularone:
                        indexonhead(automate, e[1], head, nb - 1)
                    elif e[0] == regular:
                        for wrd in e[1]:
                            indexonhead(automate, wrd, head, nb - 1)
                    elif e[0] == tokenplus:
                        for wrd in e[1]:
                            indexonhead(automate, wrd, head, nb)
                        e[0] = tokenstar
                        rule.append(e)
                    elif e[0] == tokenplusone:
                        indexonhead(automate, e[1], head, nb)
                        e[0] = tokenstarone
                        rule.append(e)
                    elif e[0] == tokenrgx:
                        indexonheadrgx(automate["_**_"], e[1], head)
                    elif e[0] == tokenrgxplus:
                        indexonheadrgx(automate["_**_"], e[1], head)
                        e[0] = tokenrgxstar
                        rule.append(e)
                    else:
                        erreur(','.join(w), "A rule cannot start with such an element")
                else:
                    rule.append(e)
        automate[head] = rule[:]
    return automate


# ------------------------------------------------------------------------------
# There are two ways to compile your code
# Either you don't have capsules in your rules and you can call compile(lex)
# Or you have capsules, then you need to call: compilecapsules(lex, locals())
# ------------------------------------------------------------------------------

def compile(lex):
    if type(lex) == list:
        v = lex
    else:
        v = lex.split("\n")
    return compiling(v, {})


# ------------------------------------------------------------------------------
# functions is actually the results of calling: locals()
# compilecapsules(lex, locals())
# locals() is used to access your own capsule functions that should be defined in
# space where compilecapsules is called from
# ------------------------------------------------------------------------------

def compilecapsules(lex, functions):
    if type(lex) == list:
        v = lex
    else:
        v = lex.split("\n")
    return compiling(v, functions)


# ------------------------------------------------------------------------------
# Below are the different functions that are called from within rules
# ------------------------------------------------------------------------------
def anytoken(tokens, sz, rl, rnxt, pos):
    return pos + 1


def regularone(tokens, sz, rl, rnxt, pos):
    if tokens[pos] == rl[1]:
        return pos + 1
    return -1


def regular(tokens, sz, rl, rnxt, pos):
    if tokens[pos] in rl[1]:
        return pos + 1
    return -1


def multiple(tokens, sz, rl, rnxt, pos):
    for r in rl[1]:
        if r[0](tokens, sz, r, once, pos) != -1:
            return pos + 1
    return -1


def optionalone(tokens, sz, rl, rnxt, pos):
    if tokens[pos] == rl[1]:
        return pos + 1
    return pos


def optional(tokens, sz, rl, rnxt, pos):
    if tokens[pos] in rl[1]:
        return pos + 1
    return pos


def optionalrgx(tokens, sz, rl, rnxt, pos):
    if re.match(rl[1], tokens[pos]):
        return pos + 1
    return pos


def optionalcapsule(tokens, sz, rl, rnxt, pos):
    func = rl[1]
    if func(tokens, pos, rnxt):
        return pos + 1
    return pos


def optionalmultiple(tokens, sz, rl, rnxt, pos):
    while pos < sz:
        found = False
        for r in rl[1:]:
            if r[0](tokens, sz, r, once, pos) != -1:
                found = True
                break
        if not found:
            return pos
        pos += 1
    return pos


def tokenrgx(tokens, sz, rl, rnxt, pos):
    if re.match(rl[1], tokens[pos]):
        return pos + 1
    return -1


def tokenstarone(tokens, sz, rl, rnxt, pos):
    while pos < sz and tokens[pos] == rl[1]:
        pos += 1
    return pos


def tokenplusone(tokens, sz, rl, rnxt, pos):
    if tokens[pos] == rl[1]:
        pos += 1
        while pos < sz and tokens[pos] == rl[1]:
            pos += 1
        return pos
    return -1


def tokenstar(tokens, sz, rl, rnxt, pos):
    while pos < sz and tokens[pos] in rl[1]:
        pos += 1
    return pos


def tokenplus(tokens, sz, rl, rnxt, pos):
    if tokens[pos] in rl[1]:
        pos += 1
        while pos < sz and tokens[pos] in rl[1]:
            pos += 1
        return pos
    return -1


# A capsule is called with !function_name
def capsule(tokens, sz, rl, rnxt, pos):
    func = rl[1]
    if func(tokens, pos, rnxt):
        return pos + 1
    return -1


# -----------------------------------------------------------------------------
# Pseudo functions to test on the next element
# -----------------------------------------------------------------------------
# This one is provided when the complex element is the last of the rule
def never(tokens, sz, rl, rnxt, pos):
    return -1


# This one allows only for one test
def once(tokens, sz, rl, rnxt, pos):
    return pos


# -----------------------------------------------------------------------------
# Complex functions that depends on the next element
# -----------------------------------------------------------------------------
def anystar(tokens, sz, rl, rnxt, pos):
    fnext = rnxt[0]
    while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
        pos += 1
    if pos != sz:
        return pos
    return -1


def anyplus(tokens, sz, rl, rnxt, pos):
    pos += 1
    fnext = rnxt[0]
    while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
        pos += 1
    if pos != sz:
        return pos
    return -1


def tokenrgxstar(tokens, sz, rl, rnxt, pos):
    fnext = rnxt[0]
    while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
        if not re.match(rl[1], tokens[pos]):
            return pos
        pos += 1
    return pos

def tokenrgxplus(tokens, sz, rl, rnxt, pos):
    if re.match(rl[1], tokens[pos]):
        pos += 1
        fnext = rnxt[0]
        while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
            if not re.match(rl[1], tokens[pos]):
                return pos
            pos += 1
        return pos
    return -1


def multiplestar(tokens, sz, rl, rnxt, pos):
    fnext = rnxt[0]
    while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
        found = False
        for r in rl[1]:
            if r[0](tokens, sz, r, once, pos) != -1:
                found = True
                break
        if not found:
            return pos
        pos += 1
    return pos


def multipleplus(tokens, sz, rl, rnxt, pos):
    found = False
    for r in rl[1]:
        if r[0](tokens, sz, r, once, pos):
            found = True
            break
    if found:
        pos += 1
        fnext = rnxt[0]
        while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
            found = False
            for r in rl[1]:
                if r[0](tokens, sz, r, once, pos) != -1:
                    found = True
                    break
            if not found:
                return pos
            pos += 1
        return pos
    return -1


def capsulestar(tokens, sz, rl, rnxt, pos):
    fnext = rnxt[0]
    func = rl[1]
    while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
        if not func(tokens, pos, rnxt):
            return pos
        pos += 1
    return pos

def capsuleplus(tokens, sz, rl, rnxt, pos):
    func = rl[1]
    if func(tokens[pos]):
        pos += 1
        fnext = rnxt[0]
        while pos < sz and fnext(tokens, sz, rnxt, [once], pos) == -1:
            if not func(tokens, pos, rnxt):
                return pos
            pos += 1
        return pos
    return -1


# ------------------------------------------------------------------------------
# Text tokenization with basic tokenizer
# It returns both the tokens and their initial positions
# in the string: s
# ------------------------------------------------------------------------------
punctuations = {
    0x21, 0x22, 0x23, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D,
    0x2E, 0x2F, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x5B, 0x5C,
    0x5D, 0x5E, 0x60, 0x7B, 0x7C, 0x7D, 0x7E, 0x9C, 0xA0, 0xA1, 0xA2,
    0xA4, 0xA5, 0xA6, 0xAA, 0xAB, 0xAC, 0xAD, 0xAF, 0xB0, 0xB1, 0xB5,
    0xB6, 0xB7, 0xB8, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xD7, 0xF7,
    0x2BC, 0x2013, 0x2014, 0x2015, 0x2018, 0x2019, 0x201C, 0x201D, 0x2020,
    0x2021, 0x2022, 0x2026, 0x2032, 0x2033, 0x203B, 0x212E, 0x2190, 0x2191,
    0x2192, 0x2193, 0x2264, 1470, 1472, 1475, 1478, 1523, 1524, 0x2265,
    0x263A, 0x3008, 0x3009, 1548, 1549, 1550, 1551, 1567, 1645, 1757, 1758, 1769, 0xFD3E,
    0xFD3F, 0x3001, 0xFF0C, 0x2025, 0x2026, 0x3002, 0x303D, 0x300C, 0x300D, 0x300E, 0x300F,
    0x301D, 0x301F, 0x301C, 0xff1a, 0xff01, 0xff1f, 0x266a}

spaces = {9, 10, 13, 32, 160, 0x202F, 0x3000}


def checknext(s, i, sz):
    return (i < sz and ord(s[i]) not in punctuations and ord(s[i]) not in spaces)


def tokenizing_sentence(s, offset=True):
    begintoken = 0
    tokens = []
    tokens_lower = []
    offsets = []
    atoken = False
    sz = len(s)
    # a hack to avoid taking into account the last token
    if sz and ord(s[-1]) not in spaces:
        s += " "
        sz += 1
    for i in range(sz):
        c = s[i]
        # if it is a space character
        if ord(c) in spaces:
            # there was a token construction pending
            if atoken:
                token = s[begintoken:i]
                tokens.append(token)
                token = token.lower()
                tokens_lower.append(token)
                offsets.append([begintoken, i])
                atoken = False
        elif ord(c) in punctuations:
            if atoken:
                # we accept some ponctuations as part of a string
                if c in {".", "-", "+"} and checknext(s, i + 1, sz):
                    continue
                token = s[begintoken:i]
                tokens.append(token)
                token = token.lower()
                tokens_lower.append(token)
                offsets.append([begintoken, i])
                atoken = False
            elif c in {"+", "-"} and checknext(s, i + 1, sz):
                # sign before a number: +10
                begintoken = i
                atoken = True
                continue
            tokens.append(c)
            tokens_lower.append(c)
            offsets.append([i, i + 1])
            continue
        elif not atoken:
            # we now start a token construction
            atoken = True
            begintoken = i
    if offset:
        return [tokens_lower, offsets, tokens]
    return tokens



# # We keep this version, but it poses some issues as it
# # tries to tokenize some Python code and not some text.
# def tokenize_sentence(s):
#     f = BytesIO(s.encode('utf-8'))
#     g = tokenize.tokenize(f.readline)
#     tokens = []
#     offsets = []
#     refz = ""
#     offset = 0
#     for toknum, tokval, x, y, z in g:
#         if z is not refz:
#             offset = s.find(z, offset)
#             refz = z
#         if tokval != '':
#             tokens.append(tokval.lower())
#             b = x[1] + offset
#             e = y[1] + offset
#             offsets.append([b, e])
#     return [tokens, offsets]
#

# ------------------------------------------------------------------------------
# Rule Application
# We apply a rule from position i
# ------------------------------------------------------------------------------

def checkrule(a, sz, ruleheads, tokens, i):
    for rhead in ruleheads:
        keeps = []
        rule = a[rhead]
        pos = i + 1
        err = False
        j = 0
        nb = len(rule)
        while j < nb:
            if pos == sz:
                err = True
                break
            code = rule[j][0]
            if j + 1 < len(rule):
                npos = code(tokens, sz, rule[j], rule[j + 1], pos)
            else:
                npos = code(tokens, sz, rule[j], [never], pos)
            if npos == -1:
                err = True
                break
            if not rule[j][-1]:
                # in this case, these elements
                # will be kept in the final string
                # We keep these positions to avoid removing
                # them latter on
                p = []
                for n in range(pos, npos):
                    p.append(n)
                keeps.append(p)
            j += 1
            pos = npos
        if not err:
            return [rhead.replace("…∞", ""), pos, keeps]
    return False


# parsing function, which takes a text and compiled rules as input
def parse(txt, a):
    heads = a["_++_"]
    regs = a["_**_"]
    # We tokenizing our own in-house tokenizer version...
    # The other version considers the text to be some kind of Python code
    tokens, offsets, rawtokens = tokenizing_sentence(txt)
    sz = len(tokens)
    results = []
    i = 0
    while i < sz:
        token = tokens[i]
        if token in heads:
            ruleheads = heads[token]
            ret = checkrule(a, sz, ruleheads, tokens, i)
            if ret:
                p = [offsets[i][0], offsets[ret[1] - 1][1]]
                thehead = ret[0]
                keeps = ret[-1]
                if len(keeps):
                    # If we have some elements to keep
                    # We build offsets that skip them
                    nb = 1
                    for s in keeps:
                        beg = offsets[s[0]][0]
                        end = offsets[s[-1]][1]
                        thehead = thehead.replace("%"+str(nb), txt[beg:end])
                        nb += 1
                if rawtokens[i][0].isupper():
                    thehead = thehead[0].upper() + thehead[1:]
                results.append([thehead, p])
                i = ret[1] - 1
        else:
            for reg in regs:
                if re.match(reg, token):
                    ruleheads = regs[reg]
                    ret = checkrule(a, sz, ruleheads, tokens, i)
                    if ret:
                        p = [offsets[i][0], offsets[ret[1] - 1][1]]
                        thehead = ret[0]
                        keeps = ret[-1]
                        if len(keeps):
                            # If we have some elements to keep
                            # We build offsets that skip them
                            nb = 1
                            for s in keeps:
                                beg = offsets[s[0]][0]
                                end = offsets[s[-1]][1]
                                thehead = thehead.replace("%" + str(nb), txt[beg:end])
                                nb += 1
                        if rawtokens[i][0].isupper():
                            thehead = thehead[0].upper() + thehead[1:]
                        results.append([thehead, p])
                        i = ret[1] - 1
                        break
        i += 1
    results.reverse()
    return results