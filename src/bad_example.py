import os
import subprocess

password = "admin123"


def run(cmd):
    return subprocess.call(cmd, shell=True)


def calc(expr):
    return eval(expr)


def check(user):
    assert user is not None
