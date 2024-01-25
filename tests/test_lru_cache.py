import pytest
from simplememcache.lru import LRUCache


class TestLruCache:
    def test__MoreElementsInserted__LRUElementDeleted(self):
        # Given
        c = LRUCache[str](3)
        c.insert("1", "1")
        c.insert("2", "2")
        c.insert("3", "3")
        assert c.key_order == ["3", "2", "1"]
        c.insert("4", "4")

        # When-Then
        with pytest.raises(KeyError):
            c.get("1")

        assert len(c.key_order) == 3
        assert c.size == 3
        assert c.key_order == ["4", "3", "2"]

    def test__MoreElementsInsertedAfterAccessing__LRUElementDeleted(self):
        # Given
        c = LRUCache[str](3)
        c.insert("1", "1")
        c.insert("2", "2")
        c.insert("3", "3")

        # When
        c.get("1")  # this should move 1 to the front and 2 to the tail
        assert c.key_order == ["1", "3", "2"]
        c.insert("4", "4")  # this should delete 2 since it's the LRU element

        # Then
        with pytest.raises(KeyError):
            c.get("2")

        assert len(c.key_order) == 3
        assert c.size == 3
        assert c.key_order == ["4", "1", "3"]

    def test__AccessingDeletingAndThenInserting__LRUOrderIsMaintained(self):
        # Given
        c = LRUCache[str](3)
        c.insert("1", "1")
        c.insert("2", "2")
        c.insert("3", "3")

        # When
        c.get("1")  # this should move 1 to the front and 2 to the tail

        # Then
        assert c.key_order == ["1", "3", "2"]

        # When
        c.delete("3")  # this should delete 3
        assert c.key_order == ["1", "2"]
        c.insert("4", "4")
        assert c.key_order == ["4", "1", "2"]
        c.insert("5", "5")
        assert c.key_order == ["5", "4", "1"]

        # Then
        with pytest.raises(KeyError):
            c.get("2")

        assert len(c.key_order) == 3
        assert c.size == 3
        assert c.key_order == ["5", "4", "1"]
        c.get("1")
        assert c.key_order == ["1", "5", "4"]
        c.get("5")
        assert c.key_order == ["5", "1", "4"]
