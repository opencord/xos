import os
import re
import signal
import sys

def handler(signum, frame):
    print "Timed Out"
    sys.exit(-1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(60) # timeout in 60 seconds

waitlines = open(sys.argv[1]).readlines()
waitlines = [x.strip() for x in waitlines]

while True:
    if not waitlines:
        print "all lines matched"
        break
    line=sys.stdin.readline()
    line=line.strip()
    for pattern in waitlines[:]:
        if re.match(pattern, line):
            print "matched", pattern
            waitlines.remove(pattern)
