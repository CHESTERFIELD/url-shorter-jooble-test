import hashlib
import base64


class UrlShorterHelper(object):
    """Class used to shorten given urls."""

    @staticmethod
    def get_unique_hash_url(url: str) -> str:
        print(url)
        url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        url_byte_array = bytearray()
        url_byte_array.extend(map(ord, url_hash))
        last_seven_bytes = url_byte_array[-7:]
        return base64.b64encode(last_seven_bytes).decode("utf-8")[:-2]
