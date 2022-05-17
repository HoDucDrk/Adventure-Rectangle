from os import walk


def takeImage(path):
    for _, _, img_name in walk(path):
        name = img_name
    return name

    