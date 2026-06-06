import os
import sys
from copy_static import copy_directory
from generate_page import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy_directory(os.path.join(base, "static"), os.path.join(base, "docs"))
    generate_pages_recursive(
        os.path.join(base, "content"),
        os.path.join(base, "template.html"),
        os.path.join(base, "docs"),
        basepath,
    )


main()
