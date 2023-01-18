import unittest
from simplememcache.lru_cache import LRUCache

class TestLruCache(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert_size_check(self):
        c = LRUCache[str](3)
        c.insert("1", "1")
        c.insert("2", "2")
        c.insert("3", "3")
        c.insert("4", "4")
        with self.assertRaises(KeyError):
            c.get("1")
        
        self.assertEqual(len(c.key_order), 3)
        self.assertEqual(c.key_order, ["4", "3", "2"])
        

    def test_lru_and_size_with_get(self):
        c = LRUCache[str](3)
        c.insert("1", "1")
        c.insert("2", "2")
        c.insert("3", "3")
        c.get("1")
        c.insert("4", "4")
        with self.assertRaises(KeyError):
            c.get("2")

        self.assertEqual(len(c.key_order), 3)
        self.assertEqual(c.key_order, ["4", "1", "3"])

    def test_lru_and_size_and_delete(self):
        c = LRUCache[str](3)
        c.insert("1", "1")
        c.insert("2", "2")
        c.insert("3", "3")
        c.get("1")
        self.assertEqual(c.key_order, ["1", "3", "2"])
        c.delete("3")
        c.insert("4", "4")
        c.insert("5", "5")
        print(c.key_order)
        with self.assertRaises(KeyError):
            c.get("2")
        
        self.assertEqual(len(c.key_order), 3)
        self.assertEqual(c.key_order, ["4", "1", "3"])
        


if __name__ == "__main__":
    unittest.main()