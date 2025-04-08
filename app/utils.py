import os

def ensure_dirs():
    """Ensure all required directories exist"""
    dirs = [
        "./data",
        "./data/custom_registries",
        "./data/vector_stores",
        "./data/cache"
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)