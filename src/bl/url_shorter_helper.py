import hashlib
import base64
import string
from random import choices

from models import UrlModel


class UrlShorterHelper(object):
    """Class used to shorten given urls."""

    @staticmethod
    def get_unique_hash_url(url: str) -> str:
        # url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        # url_byte_array = bytearray()
        # url_byte_array.extend(map(ord, url_hash))
        # last_seven_bytes = url_byte_array[-7:]
        # url_hash = base64.b64encode(last_seven_bytes).decode("utf-8")[:-2]
        characters = string.digits + string.ascii_letters
        url_hash = ''.join(choices(characters, k=7))

        if UrlModel.query.filter_by(url_hash=url_hash).first():
            return UrlShorterHelper.get_unique_hash_url(url)

        return url_hash
