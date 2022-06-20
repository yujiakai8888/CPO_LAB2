import copy
class HashMap(object):

    def __init__(self, size=5):
        self.__curr__ = 0
        self.len = size
        self.data = []
        self.keynumber = 0
        for i in range(size):
            self.data.append([])

    # 11.iteration and __next__
    def __iter__(self):
        return self

    def __next__(self):
        if self.keynumber > 0:
            if self.__curr__ < self.keynumber:
                cur = self.__curr__
                for i in range(self.len):
                    if cur >= len(self.data[i]):
                        cur -= len(self.data[i])
                        continue
                    else:
                        tmp = self.data[i][cur]
                        self.__curr__ += 1
                        return tmp
            else:
                self.__curr__ = 0
                raise StopIteration
        else:
            raise StopIteration


# 1. cons
def cons(key, hashmap):
    new = HashMap()
    new.data = copy.deepcopy(hashmap.data)
    new.len = hashmap.len
    new.keynumber = hashmap.keynumber
    new.__curr__ = hashmap.__curr__

    if member(key, hashmap):
        return new

    if key is None:
        index = 0
    else:
        index = key % new.len
    new.data[index].append(key)
    new.keynumber += 1
    return new


# 2. remove
def remove(hashmap, key):
    new = HashMap()
    new.data=copy.deepcopy(hashmap.data)
    new.len = hashmap.len
    new.keynumber = hashmap.keynumber
    new.__curr__ = hashmap.__curr__

    if key is None:
        index = 0
    else:
        index = key % new.len
    new.keynumber -= 1
    for value in new.data[index]:
        if value == key:
            new.data[index].remove(value)
    return new


# 3. length
def length(hashmap):
    return hashmap.keynumber


# 4. member
def member(key, hashmap):
    for layer1 in hashmap.data:
        for layer2 in layer1:
            if key == layer2:
                return True
    return False


# 5. intersection
def intersection(hashmap1, hashmap2):
    new = HashMap()
    set1 = set()
    for layer1 in hashmap1.data:
        for layer2 in layer1:
            set1.add(layer2)
    set2 = set()
    for layer1 in hashmap2.data:
        for layer2 in layer1:
            set2.add(layer2)
    set3 = set1.intersection(set2)
    for v in set3:
        new = cons(v, new)
    return new


# 6. conversion
def from_list(list_A):
    new = HashMap()
    for index, value in enumerate(list_A):
        new = cons(value, new)
    return new


def to_list(hashmap):
    list_A = []
    for i in range(hashmap.len):
        for v in hashmap.data[i]:
            list_A.append(v)
    return list(set(list_A))


# 7. concat
def concat(hashmap1, hashmap2):
    new = HashMap()
    list1 = to_list(hashmap1)
    list2 = to_list(hashmap2)
    list = list1 + list2
    new = from_list(list)
    return new


# 8. filter: return a list
def filter(hashmap, func):
    res = []
    for i in range(hashmap.len):
        for v in hashmap.data[i]:
            if func(v):
                res.append(v)
    return res


# 9.map(func): return a list
def map(hashmap, func):
    res = []
    for i in range(hashmap.len):
        for v in hashmap.data[i]:
            res.append(func(v))
    return res


# 10.reduce: return accumulator
def reduce(hashmap, func, initial):
    accumulator = initial
    for i in range(hashmap.len):
        for v in hashmap.data[i]:
            accumulator = func(accumulator, v)
    return accumulator


# 11.monoid_add
def monoid_add(hashmap, another_hash):
    if another_hash.keynumber == 0:
        return hashmap
    list1 = to_list(hashmap)
    list2 = to_list(another_hash)
    list = list1 + list2
    new = from_list(list)
    return new
