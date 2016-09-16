#!/usr/bin/python
from sys import argv,exit
import re
import os.path
import random



KEEP_SITE_ARG = '--keep-site'
if KEEP_SITE_ARG in argv:
    argv.remove(KEEP_SITE_ARG)
    KEEP_SITE = True
else:
    KEEP_SITE = False
    
#Parse arguments
if len(argv)!=3:
    print ("Generate username and passwords\nUsage: {exe} PC2_Team.tab users[.txt] [--keep-site]".format(exe=argv[0]))
    exit(1)
    
USERS = argv[1]
OUTPUT = argv[2]
if not OUTPUT:
    OUTPUT = 'users'
if not OUTPUT.endswith('.txt'):
    OUTPUT += '.txt'

def genpass():
    alphabet = "abcdefghijkmnopqrstuvwxyz23456789?."
    pw_length = 6
    return ''.join([alphabet[random.randrange(len(alphabet))] for _ in range(pw_length)])

# Parse users file and generate output
with open(OUTPUT, "w") as out:
    out.write("[user]\n")
    with open(USERS, "r") as users:
        for i,line in enumerate(users):
            data = [s.strip() for s in line.split('\t')]
            user = {}
            name = data[3]
            university = data[5]
            user['usernumber'] = data[0]
            user['usericpcid'] = data[0]
            user['username'] = 'team' + str(i+1)
            user['userfullname'] = name + ' - ' + university
	    user['userdesc'] = university
            user['userpassword']  = genpass()
            if KEEP_SITE:
                user['usersitenumber'] = data[1] #un
            else:
                user['usersitenumber'] = '1'
            user['userenabled'] = 't'
            for k,v in user.items():
                out.write(k+'='+v+'\n')
            out.write('\n')


