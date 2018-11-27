#!/usr/bin/env python

from string import lowercase, uppercase, letters, digits
from itertools import product, imap, repeat


def product_passwords(st, length):
  return imap(lambda i: ''.join(i), product(*repeat(st, length)))


def generate_passwords(policy, length):
  return product_passwords(eval(policy), length)

if __name__ == '__main__':
  from sys import argv
  policy, length, output = argv[1:]
  length = int(length)
  fd = open(output, 'w')
  for p in generate_passwords(policy, length):
    fd.write(p + '\n')
