import random, copy, struct
import hashlib
import numpy as np
 
def sha1_hash32(data):
    return struct.unpack('<I', hashlib.sha1(data).digest()[:4])[0]
_mersenne_prime = (1 << 61) - 1
_max_hash = (1 << 32) - 1
_hash_range = (1 << 32)
 
 
class MinHash(object):
 
    def __init__(self, d=128, seed=1,
            hashfunc=sha1_hash32,
            hashvalues=None, permutations=None):
        if hashvalues is not None:
            d = len(hashvalues)
        self.seed = seed
        # Check the hash function.
        if not callable(hashfunc):
            raise ValueError("The hashfunc must be a callable.")
        self.hashfunc = hashfunc
    
        # Initialize hash values
        if hashvalues is not None:
            self.hashvalues = self._parse_hashvalues(hashvalues)
        else:
            self.hashvalues = self._init_hashvalues(d)
        if permutations is not None:
            self.permutations = permutations
        else:
            generator = np.random.RandomState(self.seed)
            self.permutations = np.array([(generator.randint(1, _mersenne_prime, dtype=np.uint64),
                                           generator.randint(0, _mersenne_prime, dtype=np.uint64))
                                          for _ in range(d)], dtype=np.uint64).T
        if len(self) != len(self.permutations[0]):
            raise ValueError("Numbers of hash values and permutations mismatch")
 
    def _init_hashvalues(self, d):
        return np.ones(d, dtype=np.uint64)*_max_hash
 
    def _parse_hashvalues(self, hashvalues):
        return np.array(hashvalues, dtype=np.uint64)
 
    def add(self, b):
 
        hv = self.hashfunc(b)
        a, b = self.permutations
        phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash))
        self.hashvalues = np.minimum(phv, self.hashvalues)
 
    def jaccard(self, other):
 
        if other.seed != self.seed:
            raise ValueError("different seeds")
        if len(self) != len(other):
            raise ValueError("different numbers of permutation functions")
        return np.float(np.count_nonzero(self.hashvalues==other.hashvalues)) /  np.float(len(self))
 
 
    def __len__(self):
        return len(self.hashvalues)
 
    def __eq__(self, other):
        return type(self) is type(other) and  self.seed == other.seed and np.array_equal(self.hashvalues, other.hashvalues)