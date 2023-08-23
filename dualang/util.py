import xattr


def add_label_to_file(file_path: str, label: str):
    xattr.setxattr(file_path, "com.apple.metadata:_kMDItemUserTags", label.encode())
