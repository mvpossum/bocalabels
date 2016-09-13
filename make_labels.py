#!/usr/bin/python
from sys import argv,exit
import re
import os.path
from subprocess import call

#Parse arguments
if len(argv)!=5:
    print ("Creates a pdf with the labels\nUsage: {exe} contest_name users.tab passwords.tab output[.tex]".format(exe=argv[0]))
    exit(1)

CONTEST_NAME = argv[1]
USERS = argv[2]
PASSWORDS = argv[3]
OUTPUT = argv[4]
if not OUTPUT.endswith('.tex'):
    OUTPUT += '.tex'
    
#Parse Template
with open (os.path.join(os.path.dirname(__file__), "templatelabels.tex"), "r") as tf:
    raw = tf.read()
raw = raw.replace('%CONTEST NAME%', CONTEST_NAME)
[(head, tail)] = re.compile("(.*)%USERS_WILL_GO_HERE%(.*)", re.DOTALL).findall(raw)


# Parse Passwords file
passwords = {}
with open(PASSWORDS, "r") as pas:
    for line in pas:
        data = [s.strip() for s in line.split('\t')]
        passwords[data[1]] = data[2]


def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)
    
# Parse users file and generate tex
with open(OUTPUT, "w") as out:
    out.write(head)
    with open(USERS, "r") as users:
        for line in users:
            data = [s.strip() for s in line.split('\t')]
            user = tex_escape(data[0])
            if user not in passwords:
                print("Couldn't find password for team %s." % user)
                exit(1)
            user = tex_escape(user)
            password = tex_escape(passwords[user])
            name = tex_escape(data[3])
            if max([len(s) for s in name.split(' ')])>20: #avoid overflow
                name = '{\\normalsize '+name+'}'
            
            university = tex_escape(data[5])
            out.write("\\user{%s}{%s}{%s}{%s}\n\n"
                % (university, name, user, password))
    out.write(tail)

# Compile tex into pdf
call(["pdflatex", OUTPUT])
