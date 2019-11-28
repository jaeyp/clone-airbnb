import ntpath
from inspect import getframeinfo, stack


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def info(message):
    caller = getframeinfo(stack()[1][0])
    print(f"{path_leaf(caller.filename)}:{caller.lineno} - {message}")
