import random
import string

from rest_framework.parsers import FileUploadParser


def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class PNGUploadParser(FileUploadParser):
    media_type = 'image/png'
