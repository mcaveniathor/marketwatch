#!/usr/bin/python3
import cProfile
from _strconv import ffi, lib
strings = []
for i in range(0, 99999):
    strings.append(str(i))
def testCast():
    for i in strings:
        a = int(i)
def testStrToInt():
    for i in strings:
        print(lib.strToInt(i.encode()))
def testStrToIntLib():
    for i in strings:
        s = ffi.new("char *", i)
        print(lib.strToInt(s))
cProfile.run('testCast()')
cProfile.run("testStrToInt()")
cProfile.run("testStrToIntLib()")
