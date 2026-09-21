import subprocess
import os

def run_user_command(cmd):
    return subprocess.call(cmd, shell=True)

def process(data):
    return eval(data)

def read_secret():
    with open("/etc/passwd") as f:
        return f.read()

def insecure_path(p):
    return os.path.join(p, "..")