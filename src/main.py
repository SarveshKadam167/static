import os
from copy_static import copy_directory
from generate_page import generate_pages_recursive


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy_directory(os.path.join(base, "static"), os.path.join(base, "public"))
    generate_pages_recursive(
        os.path.join(base, "content"),
        os.path.join(base, "template.html"),
        os.path.join(base, "public"),
    )


main()
