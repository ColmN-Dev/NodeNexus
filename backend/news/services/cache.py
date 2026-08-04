import time


class TTLCache:
    """
    Simple in-memory cache with a time-to-live per entry.
    Not persistent across restarts/workers.
    """

    # -----------------------------
    # INIT
    # -----------------------------
    def __init__(self, duration_seconds):
        self._duration = duration_seconds
        self._store = {}

    #-----------------------------
    # GET / SET
    #-----------------------------
    def get(self, key):
        entry = self._store.get(key)

        if entry is None:
            return None

        saved_time, data = entry

        # Check if the entry has expired
        if time.time() - saved_time >= self._duration:
            del self._store[key]
            return None

        return data

    # Add a method to set data in the cache
    def set(self, key, data):
        self._store[key] = (time.time(), data)