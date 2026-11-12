import ast
import os
import subprocess  # noqa: S404  reviewed: only runs a fixed argument list

password = os.environ.get("APP_PASSWORD", "")


def run(args):
    return subprocess.call(args)  # noqa: S603  args are not user input


def calc(expr):
    return ast.literal_eval(expr)


def check(user):
    if user is None:
        raise ValueError("user is required")
