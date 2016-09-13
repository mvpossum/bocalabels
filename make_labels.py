#!/usr/bin/python
from sys import argv,exit
import re
import os.path
from subprocess import call

#Parse arguments
if len(argv)!=4:
    print ("Creates a pdf with the labels\nUsage: {exe} contest_name users.txt labels[.tex]".format(exe=argv[0]))
    exit(1)

CONTEST_NAME = argv[1]
USERS = argv[2]
OUTPUT = argv[3]
if not OUTPUT.endswith('.tex'):
    OUTPUT += '.tex'
    
#Parse Template
with open (os.path.join(os.path.dirname(__file__), "templatelabels.tex"), "r") as tf:
    raw = tf.read()
raw = raw.replace('%CONTEST NAME%', CONTEST_NAME)
[(head, tail)] = re.compile("(.*)%USERS_WILL_GO_HERE%(.*)", re.DOTALL).findall(raw)

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
    
def parse_user(data):
    attrs = {}
    for l in data.split('\n'):
        p = l.find('=')
        attrs[l[:p].strip()] = l[p+1:].strip()
    return attrs
    
# Parse users file and generate tex
with open(OUTPUT, "w") as out:
    out.write(head)
    with open(USERS, "r") as users:
        users.readline()
        config = users.read()
    for data in config.split('\n\n'):
        if data:
            user =  parse_user(data)
            print(user)
            username = tex_escape(user['username'])
            password = tex_escape(user['userpassword'])
            university = tex_escape(user['userdesc'])
            name = tex_escape(user['userfullname'][:-(3+len(university))])
            if max([len(s) for s in name.split(' ')])>20: #avoid overflow
                name = '{\\normalsize '+name+'}'
            
            out.write("\\user{%s}{%s}{%s}{%s}\n\n"
                % (university, name, username, password))
    out.write(tail)

# Compile tex into pdf
call(["pdflatex", OUTPUT])
