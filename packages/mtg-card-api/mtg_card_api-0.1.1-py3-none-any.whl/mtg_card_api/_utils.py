import hashlib


def encodeMD5(str):
    """Converts a string into its MD5 representation string"""
    return hashlib.md5(str.encode()).hexdigest()
