class ObjectPool:
    def __init__(self, create_func, max_size=10):
        self._create_func = create_func
        self._pool = []
        self._max_size = max_size
        self._total_created = 0

    @property
    def total_created(self):
        return self._total_created

    def acquire(self):
        if self._pool:
            return self._pool.pop()
        else:
            self._total_created += 1
            return self._create_func()

    def release(self, obj):
        if len(self._pool) < self._max_size:
            self._pool.append(obj)