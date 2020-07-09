#!/usr/bin/python

import crypt
import subprocess
import time
import sys

if len(sys.argv)==2:
	passFile = sys.argv[1]
else:
	print "[-] Usage ./linuxpassdecrypt.py <passFile>"
	sys.exit()


output = subprocess.check_output('ls /home/', shell=1)
users = output.split('\n')
users.append('root')

print "Available Users\n"
for count, user in enumerate(users):
	print count, " " ,user

choice = raw_input("Enter user >> ")
try:
	key = users[int(choice)]
except:
	print "[-] Invalid Choice, Run it again"

command = 'grep '+key+' /etc/shadow'
op = subprocess.check_output(command, shell=1)
salt='$'+op.split('$')[1]+'$'+op.split('$')[2]
actualHash = op.split(":")[1]

try:
	f=open(passFile, 'r')
except:
	print "[-] File not found"
counter=0
for password in f:
	start = time.time()
	counter=counter+1
	hash = crypt.crypt(password.strip(), salt)
	if hash == actualHash:
		stop = time.time()
		timeTaken = stop - start
		print"[+] Password found", password
		print "[+] Tried ", counter, "password"
		print "[+] Time taken", timeTaken
		break
else:
	print "[-] Password not found"
	print "Tired", counter, "passwords"
