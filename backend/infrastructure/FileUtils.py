import os


def get_extension(name):
    _, ext = os.path.splitext(name)
    return ext[1:]
