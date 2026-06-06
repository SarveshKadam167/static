import os
from copy_static import copy_directory


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(base, "static")
    dst = os.path.join(base, "public")
    copy_directory(src, dst)


main()
