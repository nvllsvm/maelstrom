import hashlib


def hash_str(value):
    h = hashlib.sha256()
    h.update(value.encode())
    return h.hexdigest()
