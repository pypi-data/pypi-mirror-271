"""
def get_md5_str(s: str)
"""

import hashlib


def get_md5_str(s: str):
    return hashlib.md5(s.encode()).hexdigest()
