import threading


class MultitonMeta(type):
    _instances = {}
    _lock: threading.Lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        if not args:
            raise ValueError("Multiton must be initialized with a key argument")

        key = args[0]
        with cls._lock:
            if key not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[key] = instance
        return cls._instances[key]
