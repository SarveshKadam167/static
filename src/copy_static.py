import os
import shutil


def copy_directory(src, dst):
    if os.path.exists(dst):
        print(f"Deleting {dst}")
        shutil.rmtree(dst)
    os.mkdir(dst)
    _copy_recursive(src, dst)


def _copy_recursive(src, dst):
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            _copy_recursive(src_path, dst_path)
