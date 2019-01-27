# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import subprocess

def EvalHmnBot(commands):
    commands = " ".join(commands[:])
    p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    out = ""
    for line in p.stdout.readlines():
        out += line + "\n"
        print(line)
    return_val = p.wait()

    return out

