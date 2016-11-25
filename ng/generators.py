'''
Set generators
'''

import itertools
import math
import numpy as np
import random

from scipy.stats import erlang, gamma

RANGE_MAX = 100

class Root:
    def __init__(self, h1):
        self.bitwise = h1.bitwise
        self.numeric = h1.numeric

class Generator:
    def __init__(self):
        self.arguments = None
        self.probability = None
        self.bitwise = []
        self.numeric = []
        self.sort_order = None
        
    def __str__(self):
        return self.__class__.__name__ + ' (' + ', '.join([str(s) for s in self.arguments]) + ')'

    @staticmethod
    def sample():
        pass

    @staticmethod
    def generate_all():
        pass
    
class Operator:
    def __init__(self):
        self.operands = None

    def __str__(self):
        return self.__class__.__name__ + ' (' + ', '.join([str(o) for o in self.operands]) + ')'

class Primes(Generator):
    cache = None

    def __init__(self):
        self.arguments = ()
        self.numeric = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                                 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97],
                                dtype=int)
        self.bitwise = np.array([1 if i in self.numeric else 0 for
                                 i in range(1, RANGE_MAX+1)],
                                dtype=int)
        self.probability = 1.0
        
    @staticmethod
    def sample(data=None):
        if Primes.cache == None:
            Primes.cache = Primes()
        return Primes.cache

    @staticmethod
    def generate_all():
        particles = [Primes()]
        return particles
    
class Multiples(Generator):
    cache = {}

    def __init__(self, num):
        self.arguments = (num,)
        self.bitwise = np.array([1 if (i % num) == 0 else 0 for i in 
                                 range(1, RANGE_MAX+1)], dtype=int)
        self.numeric = np.nonzero(self.bitwise)[0] + 1
        self.probability = 1./(11-2)
        
    @staticmethod
    def sample(data=None):
        arg = np.random.randint(2, 11)
        try:
            return Multiples.cache[arg]
        except:
            Multiples.cache[arg] = Multiples(arg)
            return Multiples.cache[arg]

    @staticmethod
    def generate_all():
        particles = []
        for i in range(2, 11):
            particles.append(Multiples(i))
        return particles
        
def find_start(int_size, data):
    sort_data = sorted(data)
    choices = {}
    
    if (RANGE_MAX-int_size+1 == 1):
        return 1
    
    for i in range(1, RANGE_MAX-int_size+1):
        num_covered = len([d for d in sort_data if
                           i <= d < i + int_size])
        choices.setdefault(num_covered, [])
        choices[num_covered].append(i)
        
    max_covered = max(choices.keys())
    return random.choice(choices[max_covered])
    
class Interval(Generator):
    cache = {}

    def __init__(self, start, end):
        assert end <= RANGE_MAX
        self.arguments = (start, end)
        self.bitwise = np.array([1 if (start <= i <= end) else 0 for
                                 i in range(1, RANGE_MAX+1)], dtype=int)
        self.numeric = np.nonzero(self.bitwise)[0] + 1
        
        gamma_rv = gamma(2, loc=0, scale=10)
        size = end-start
        size_prob = gamma_rv.cdf(size+1) - gamma_rv.cdf(size) # because we do int(floor(x))
        start_prob = 1./(RANGE_MAX+1-size)
        self.probability = size_prob * start_prob

    @staticmethod
    def sample(data=None):
        size = RANGE_MAX
        while size >= RANGE_MAX:
            size = int(math.floor(np.random.gamma(1.5, 10)))
        start = np.random.randint(1, RANGE_MAX+1-size)
        end = start+size

        try:
            return Interval.cache[(start, end)]
        except:
            Interval.cache[(start, end)] = Interval(start, end)
            return Interval.cache[(start, end)]

    @staticmethod
    def generate_all():
        particles = []
        for i in range(1, RANGE_MAX+1):
            for j in range(i, RANGE_MAX+1):
                particles.append(Interval(i, j))
        return particles
                
class NumbergameInterval(Generator):
    cache = {}

    def __init__(self, start, end):
        assert end <= RANGE_MAX
        self.arguments = (start, end)
        self.bitwise = np.array([1 if (start <= i <= end) else 0 for
                                 i in range(1, RANGE_MAX+1)], dtype=int)
        self.numeric = np.nonzero(self.bitwise)[0] + 1
        
        erlang_rv = erlang(2, loc=0, scale=10)
        size = end-start+1
        size_prob = erlang_rv.pdf(size)
        start_prob = 1./(RANGE_MAX+1-size)
        self.probability = size_prob / float(5050)
        
    @staticmethod
    def generate_all():
        particles = []
        for i in range(1, RANGE_MAX+1):
            for j in range(i, RANGE_MAX+1):
                particles.append(NumbergameInterval(i, j))
        return particles

class Powers(Generator):
    cache = {}

    def __init__(self, num):
        self.arguments = (num,)
        self.numeric = np.array([num**i for i in itertools.takewhile(
                    lambda x: num**x<(RANGE_MAX+1),
                    range(0, RANGE_MAX))], dtype=int)
        self.bitwise = np.array([1 if i in self.numeric else 0 for
                                 i in range(1, RANGE_MAX+1)], dtype=int)
        self.probability = 1./(4-2)

    @staticmethod
    def sample(data=None):
        arg = np.random.randint(2, 4)
        try:
            return Powers.cache[arg]
        except:
            Powers.cache[arg] = Powers(arg)
            return Powers.cache[arg]

    @staticmethod
    def generate_all():
        particles = []
        for i in range(2, 4):
            particles.append(Powers(i))
        return particles
        
class Contains(Generator):
    cache = {}

    def __init__(self, num):
        assert len(str(num)) == 1
        self.arguments = (num,)
        self.bitwise = np.array([1 if str(num) in str(i) else 0 
                                 for i in range(1, RANGE_MAX+1)], dtype=int)
        self.numeric = np.nonzero(self.bitwise)[0] + 1
        self.probability = 1./(10-1)

    @staticmethod
    def sample(data=None):
        arg = np.random.randint(1, 10)
        try:
            return Contains.cache[arg]
        except:
            Contains.cache[arg] = Contains(arg)
            return Contains.cache[arg]

    @staticmethod
    def generate_all():
        particles = []
        for i in range(1, 10):
            particles.append(Contains(i))
        return particles
        
class Equals(Generator):
    cache = {}
    
    def __init__(self, num):
        assert num <= RANGE_MAX
        self.arguments = (num,)
        self.bitwise = np.zeros(RANGE_MAX, dtype=int)
        self.bitwise[num-1] = 1
        self.numeric = np.nonzero(self.bitwise)[0] + 1
        self.probability = 1./RANGE_MAX

    @staticmethod
    def sample(data=None):
        arg = np.random.randint(1, RANGE_MAX+1)
        try:
            return Equals.cache[arg]
        except:
            Equals.cache[arg] = Equals(arg)
            return Equals.cache[arg]

    @staticmethod
    def generate_all():
        particles = []
        for i in range(1, RANGE_MAX+1):
            particles.append(Equals(i))
        return particles
        
class And(Operator):
    noperands = 2

    def __init__(self, h1, h2):
        self.operands = frozenset([h1, h2])
        self.bitwise = np.logical_and(h1.bitwise, h2.bitwise)
        self.numeric = np.nonzero(self.bitwise)[0] + 1

class Or(Operator):
    noperands = 2

    def __init__(self, h1, h2):
        self.operands = frozenset([h1, h2])
        self.bitwise = np.logical_or(h1.bitwise, h2.bitwise)
        self.numeric = np.nonzero(self.bitwise)[0] + 1

class Not(Operator):
    noperands = 1

    def __init__(self, h1):
        self.operands = (h1)
        self.bitwise = np.logical_not(h1.bitwise)
        self.numeric = np.nonzero(self.bitwise)[0] + 1
