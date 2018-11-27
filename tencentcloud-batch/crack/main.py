#!/usr/bin/env python


if __name__ == '__main__':
  from sys import argv, exit
  from os import system
  from multiprocessing import cpu_count
  from subprocess import Popen
  from time import time, sleep
  from os import environ
  cpus = cpu_count()
  ret = system('./crack/init.sh')
  sleep(10)
  if ret:
    exit(ret)
  plist = argv[1]
  index = int(environ['BATCH_TASK_INSTANCE_INDEX'])
  tasks = int(environ['BATCH_TASK_INSTANCE_NUM'])
  if tasks <= 100:
    passfile = '/root/input/DICT.%02d' % index
  else:
    passfile = '/root/input/DICT.%03d' % index
  ret = system('split -n l/%s -d %s PDICT.' % (cpus, passfile))
  if ret:
    exit(ret)
  ps = [Popen('python ./crack/crack.py %s PDICT.%02d > /root/output/crack.%s.$$.log 2>&1' % (plist, i, index), shell=True) for i in range(cpus)]
  while True:
    sleep(5)
    completed = True
    for p in ps:
      r = p.poll()
      if r:
        print 'process[%s] return error code[%s]' % (p.pid, r)
        exit(r)
      if r is None:
        completed = False
        break
    if completed:
      exit(0)
    else:
      print 'Not Completed'
