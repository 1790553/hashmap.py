class MyHashMap:

    def __init__(self, cap=13):
        self._table = cap * [None]
        self._n = 0

    def _hash_function(self, key):
        return key % len(self._table)
    
    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        self._bucket_put(j, key, value)
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)
        return self._bucket_get(j, key)

    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        self._bucket_remove(j, key)

    def __len__(self):
        return self._n


    def _bucket_put(self, j, key, value):
        bucket = self._table[j]
        if bucket is None:
            self._table[j] = [[key, value]]
            self._n += 1
            return
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._n += 1

    def _bucket_get(self, j, key):
        bucket = self._table[j]
        if bucket is None:
            return -1
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return -1

    def _bucket_remove(self, j, key):
        bucket = self._table[j]
        if bucket is None:
            return
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self._n -= 1
                if len(bucket) == 0:
                    self._table[j] = None
                return



    def _resize(self, c):
        old = self._table
        self._table = c * [None]
        self._n = 0
        for bucket in old:
            if bucket is not None:
                for key, value in bucket:
                    j = self._hash_function(key)
                    self._bucket_put(j, key, value)
