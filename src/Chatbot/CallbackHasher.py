import hashlib


class CallbackHasher:
    @staticmethod
    def hash_callback(data: str) -> str:
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    @staticmethod
    def unhash_callback(hashed: str, guesses: list[str]) -> str:
        return next(
            (
                guess
                for guess in guesses
                if hashed == hashlib.md5(guess.encode("utf-8")).hexdigest()
            ),
            None,
        )
