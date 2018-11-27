#!/usr/bin/env python

from sys import argv, exit
from os import system

num = int(argv[1])
dicts = argv[2:]
ret = system('cd /root/dicts && cat %s > _all.txt && split -n l/%s -d _all.txt /root/split_dicts/DICT.' % (' '.join(dicts), num))
print ret
exit(ret)
