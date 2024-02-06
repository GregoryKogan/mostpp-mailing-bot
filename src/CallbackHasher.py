import hashlib


class CallbackHasher:
    @staticmethod
    def hash_callback(data: str) -> str:
        return hashlib.md5(data.encode("utf-8")).hexdigest()
