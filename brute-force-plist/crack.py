#!/usr/bin/env python
from crypto.aeswrap import AESUnwrap
from keystore.keybag import Keybag, BACKUP_KEYBAG, OTA_KEYBAG, WRAP_DEVICE, WRAP_PASSCODE
from fastpbkdf2 import pbkdf2_hmac
from util import readPlist
from time import time

def crack(manifest, passwords, notify=None):
  manifest = readPlist(manifest)
  if not manifest["IsEncrypted"]:
    print "Backup is not encrypted"
    return
  iosFlag = 'ManifestKey' in manifest
  kb = Keybag(manifest["BackupKeyBag"].data)
  kb.deviceKey = None
  if kb.type != BACKUP_KEYBAG and kb.type != OTA_KEYBAG:
    print "Backup does not contain a backup keybag"
    return
  salt = kb.attrs["SALT"]
  iter = kb.attrs["ITER"]
  print 'iter', iter
  dpsl = None
  dpic = None
  if iosFlag:
    dpsl = kb.attrs["DPSL"]
    dpic = kb.attrs["DPIC"]
    print 'dpic', dpic
  res = None
  for password in passwords:
    password = password.strip()
    if not password:
      continue
    print "[%s]: Trying Crack" % (password)
    stime = time()
    res = try_password(password, iosFlag, dpsl, dpic, salt, iter, kb)
    etime = time()
    print "[%s]: Take time %s" % (password, etime - stime)
    if res:
      print 'Find Password: ', password
      return password

def try_password(password, iosFlag, dpsl, dpic, salt, iter, kb):
  if iosFlag:
    password = pbkdf2_hmac('sha256', password, dpsl, dpic, 32)
  code = pbkdf2_hmac('sha1', password, salt, iter, 32)
  for classkey in kb.classKeys.values():
    k = classkey["WPKY"]
    if classkey["WRAP"] & WRAP_PASSCODE:
      k = AESUnwrap(code, classkey["WPKY"])
      if not k:
        break
    if classkey["WRAP"] & WRAP_DEVICE:
      if not kb.deviceKey:
        continue
      k = AESdecryptCBC(k, kb.deviceKey)
  else:
    return password

if __name__ == "__main__":
  from sys import argv
  plist, passfile = argv[1], argv[2]
  res = crack(plist, open(passfile))
  if res:
    open('/tmp/password', 'w').write(res)
