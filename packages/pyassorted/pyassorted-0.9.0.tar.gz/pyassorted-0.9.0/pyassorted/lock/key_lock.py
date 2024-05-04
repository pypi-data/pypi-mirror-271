import threading
from typing import Dict, Optional, Text


class KeyLock:
    def __init__(self):
        self.locks: Dict[Text, "threading.Lock"] = {}
        self.lock_of_locks = threading.Lock()

    def __getitem__(self, key: Text) -> "threading.Lock":
        with self.lock_of_locks:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            return self.locks[key]

    def __call__(self, key: Text, *args, **kwargs) -> "threading.Lock":
        return self[key]

    def get(self, key: Text, *args, **kwargs) -> "threading.Lock":
        return self[key]

    def acquire(
        self,
        key: Text,
        blocking: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> bool:
        with self.locks_lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            key_lock = self.locks[key]
        return key_lock.acquire(blocking=blocking, timeout=timeout)

    def release(self, key: Text):
        with self.locks_lock:
            if key in self.locks:
                self.locks[key].release()

    def locked(self, key: Text):
        with self.locks_lock:
            if key in self.locks:
                return self.locks[key].locked()
            else:
                return False
