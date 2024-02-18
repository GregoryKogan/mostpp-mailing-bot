import hashlib
from enum import Enum


class CallbackType(Enum):
    EMPTY = 0
    EVENT_REGISTRATIONS = 1
    EVENT_INFO_BEFORE_SENDING_CONFIRMATIONS = 2
    EVENT_INFO_BEFORE_SENDING_THANKS = 3
    GENERATE_EMAIL = 4
    CHANGE_EVENT_DATA = 5
    CHANGE_EVENT_DATE = 6
    CHANGE_EVENT_TIME = 7
    CHANGE_EVENT_LINK = 8
    GO_BACK_FROM_CHANGING_EVENT_DATA = 9


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


def build_event_action_callback(callback_type: CallbackType, event_name: str) -> str:
    return f"{callback_type.value}${CallbackHasher.hash_callback(event_name)}"


def unhash_event_name(callback: str, registrations: dict[str, any]) -> str:
    return CallbackHasher.unhash_callback(
        callback.split("$")[1], list(registrations.keys())
    )


def parse_callback_type(callback: str) -> CallbackType:
    return CallbackType(int(callback.split("$")[0]))
