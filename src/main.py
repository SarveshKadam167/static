import os
from copy_static import copy_directory
from generate_page import generate_page


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy_directory(os.path.join(base, "static"), os.path.join(base, "public"))
    generate_page(
        os.path.join(base, "content/index.md"),
        os.path.join(base, "template.html"),
        os.path.join(base, "public/index.html"),
    )


main()
