import time


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class Cache(metaclass=Singleton):
    def __init__(self):
        self._cache = {}

    def has_key(self, key) -> bool:
        if key not in self._cache:
            return False

        record = self._cache[key]
        time_passed = time.time() - record["timestamp"]
        if time_passed > record["lifetime"]:
            self._cache.pop(key)
            return False

        return True

    def get(self, key) -> any:
        if key not in self._cache:
            return None, None

        record = self._cache[key]
        time_passed = time.time() - record["timestamp"]
        if time_passed > record["lifetime"]:
            self._cache.pop(key)
            return None, None

        return record["value"]

    def store(self, key: str, value: any, lifetime: int) -> None:
        self._cache[key] = {
            "value": value,
            "timestamp": time.time(),
            "lifetime": lifetime,
        }
