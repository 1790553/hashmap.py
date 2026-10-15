class MyHashMap:
    """Taula de hash amb encadenament separat i redimensionament.

    Cada posició de self._table és None o un bucket: una llista de
    parelles [clau, valor] de les claus que hi col·lisionen.
    Es manté el factor de càrrega n / m <= 0.5.
    """

    def __init__(self, cap=13):
        self._table = cap * [None]   # m posicions, inicialment buides
        self._n = 0                  # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)          # h(x) = x % m

    # ---------- Mètodes públics ----------

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

    # ---------- Mètodes auxiliars (treballen dins del bucket) ----------

    def _bucket_put(self, j, key, value):
        bucket = self._table[j]
        if bucket is None:                     # primer element de la posició
            self._table[j] = [[key, value]]
            self._n += 1
            return
        for pair in bucket:
            if pair[0] == key:                 # mateixa clau: actualitzem
                pair[1] = value
                return
        bucket.append([key, value])            # clau nova: l'afegim al bucket
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
                if len(bucket) == 0:           # bucket buit -> torna a None
                    self._table[j] = None
                return

    # ---------- Redimensionament ----------

    def _resize(self, c):
        old = self._table
        self._table = c * [None]               # taula nova de mida c
        self._n = 0                            # _bucket_put tornarà a comptar
        for bucket in old:
            if bucket is not None:
                for key, value in bucket:
                    j = self._hash_function(key)   # usa la mida NOVA
                    self._bucket_put(j, key, value)
