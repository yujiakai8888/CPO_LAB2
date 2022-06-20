import unittest
from hypothesis import given
import hypothesis.strategies as st
from immutable import HashMap, cons, length, remove, member, intersection, \
            to_list, from_list, concat, map, filter, reduce, monoid_add


class TestMutableHashMap(unittest.TestCase):
    def setUp(self):
        self.hashMap = HashMap()


class TestMutableHashMapMethods(TestMutableHashMap):
    def test_awpi(self):
        empty = HashMap()
        self.assertEqual(to_list(cons(None, empty)), [None])
        l1 = cons(None, cons(1, empty))
        l2 = cons(1, cons(None, empty))
        self.assertEqual(to_list(empty), [])
        self.assertTrue(to_list(l1) == [None, 1] or to_list(l1) == [1, None])
        self.assertNotEqual(to_list(empty), to_list(l1))
        self.assertNotEqual(to_list(empty), to_list(l2))
        self.assertEqual(to_list(l1), to_list(l2))
        self.assertEqual(to_list(l1), to_list(cons(None, cons(1, l1))))
        self.assertEqual(length(empty), 0)
        self.assertEqual(length(l1), 2)
        self.assertEqual(length(l2), 2)
        self.assertEqual(to_list(remove(l1, None)), [1])
        self.assertEqual(to_list(remove(l1, 1)), [None])
        self.assertFalse(member(None, empty))
        self.assertTrue(member(None, l1))
        self.assertTrue(member(1, l1))
        self.assertFalse(member(2, l1))
        self.assertEqual(to_list(intersection(l1, l2)), to_list(l1))
        self.assertEqual(to_list(intersection(l1, l2)), to_list(l2))
        self.assertEqual(to_list(intersection(l1, empty)), to_list(empty))
        self.assertEqual(to_list(intersection(
            l1, cons(None, empty))), to_list(cons(None, empty)))
        self.assertTrue(to_list(l1) == [None, 1] or to_list(l1) == [1, None])
        self.assertEqual(to_list(l1), to_list(from_list([None, 1])))
        self.assertEqual(to_list(l1), to_list(from_list([1, None, 1])))
        self.assertEqual(to_list(concat(l1, l2)),
                         to_list(from_list([None, 1, 1, None])))
        lst = to_list(l1) + to_list(l2)
        for e in l1:
            lst.remove(e)
        for e in l2:
            lst.remove(e)
        self.assertEqual(lst, [])

    def test_init(self):
        self.assertEqual(self.hashMap.len, 5)
        self.assertIsInstance(self.hashMap.data, list)
        self.assertEqual(self.hashMap.data[0], [])
        self.assertEqual(self.hashMap.data[1], [])
        self.assertEqual(self.hashMap.data[2], [])
        self.assertEqual(self.hashMap.data[3], [])
        self.assertEqual(self.hashMap.data[4], [])

    # 1. add
    def test_add(self):
        new = HashMap()
        for i in range(5):
            new = cons(i, new)
        self.assertEqual(new.data[0], [0])
        self.assertEqual(new.data[1], [1])
        self.assertEqual(new.data[2], [2])
        self.assertEqual(new.data[3], [3])
        self.assertEqual(new.data[4], [4])

    # 2. remove
    def test_remove(self):
        new = HashMap()
        new = cons(0, new)
        self.assertEqual(new.data[0], [0])
        new = remove(new, 0)
        self.assertEqual(new.data[0], [])

    # 3. length
    def test_length(self):
        self.assertEqual(length(self.hashMap), 0)

    # 4. member
    def test_member(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new = from_list(list_a)
        self.assertEqual(member(11, new), True)
        self.assertEqual(member(9, new), False)

    # 6. conversion
    def test_from_list(self):
        list_a = [0, 1, 2, 3, 4, 11]
        self.hashMap = from_list(list_a)
        self.assertEqual(self.hashMap.data[0], [0])
        self.assertEqual(self.hashMap.data[1], [1, 11])
        self.assertEqual(self.hashMap.data[2], [2])
        self.assertEqual(self.hashMap.data[3], [3])
        self.assertEqual(self.hashMap.data[4], [4])

    # 7. filter
    def test_filter(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new = from_list(list_a)

        def filterOdd(value):
            if value % 2 == 0:
                return True
            else:
                return False

        res = filter(new, filterOdd)
        self.assertEqual(res, [0, 2, 4])

    # 8.map(func)
    def test_map(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new = from_list(list_a)

        def mapPlusOne(value):
            return value + 1

        res = map(new, mapPlusOne)
        self.assertEqual(res, [1, 2, 12, 3, 4, 5])

    # 9.reduce
    def test_reduce(self):
        new = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        new = from_list(list_a)

        def reduceSum(accumulator, curr):
            return accumulator + curr

        res = reduce(new, reduceSum, 0)
        self.assertEqual(res, 21)

    # The property - based tests

    @given(st.lists(st.integers(5)))
    def test_from_list_to_list_equality(self, a):
        hash1 = HashMap()
        hash1 = from_list(a)
        b = to_list(hash1)
        a = set(a)
        b = set(b)
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        a = list(set(a))
        hash1 = HashMap()
        hash1 = from_list(a)
        self.assertEqual(length(hash1), len(a))

    # 10.monoid_add
    def test_monoid_add(self):
        hash1 = HashMap()
        hash2 = HashMap()
        list_a = [0, 1, 2, 3, 4, 11]
        list_b = [5, 6, 7]
        hash1 = from_list(list_a)
        hash2 = from_list(list_b)
        # list1 = hash1 add hash2
        list1 = to_list(monoid_add(hash1, hash2))
        # list2 = hash2 add hash1
        list2 = to_list(monoid_add(hash2, hash1))
        self.assertEqual(list1, list2)

    # 11.iteration and __next__
    def test_iter(self):
        x = [1, 2, 3]
        hash1 = HashMap()
        hash1 = from_list(x)
        tmp = []
        for e in hash1:
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(to_list(hash1), tmp)
        i = iter(HashMap())
        self.assertRaises(StopIteration, lambda: next(i))


if __name__ == "__main__":
    unittest.main()
