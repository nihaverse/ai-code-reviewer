import hashlib
import pickle
import subprocess

password = "admin123"


def run(cmd):
    subprocess.call(cmd, shell=True)


def calc(expr):
    return eval(expr)


def hash_pw(p):
    return hashlib.md5(p.encode()).hexdigest()


def load(data):
    return pickle.loads(data)


def query(cursor, name):
    cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)