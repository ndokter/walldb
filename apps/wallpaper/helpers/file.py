import hashlib


def file_hash(f):
    """
    Create sha1 hash for given File.
    """
    f.seek(0)
    h = hashlib.sha1()

    if hasattr(f, 'multiple_chunks') and f.multiple_chunks():
        for chunk in f.chunks():
            h.update(chunk)
    else:
        h.update(f.read())

    return h.hexdigest()
