from dataclasses import dataclass
from simplememcache.base_cache import BaseCache
from typing import Dict, Optional, TypeVar, Generic, List

T = TypeVar("T")


@dataclass
class LRUNode(Generic[T]):
    """
    Linked List node to maintain the LRU order
    """
    key: str
    value: T
    prev: Optional["LRUNode[T]"] = None
    next: Optional["LRUNode[T]"] = None

    def __str__(self) -> str:
        return f"Node(key={self.key}, value={self.value})"


class LRUCache(BaseCache[T]):
    __max_size: int
    __node_map: Dict[str, LRUNode[T]]
    __head: Optional[LRUNode[T]]
    __tail: Optional[LRUNode[T]]
   

    def __init__(self, max_size: int) -> None:
        assert max_size >= 0 , "Invalid cache size"
        self.__max_size = max_size
        self.__node_map = {}
        self.__head = None
        self.__tail = self.__head
        super().__init__()

    @property
    def max_size(self) -> int:
        return self.__max_size

    @property
    def size(self) -> int:
        return len(self.__node_map)

    @property
    def key_order(self) -> List[str]:
        curr = self.__head
        res = []
        while curr:
            res.append(curr.key)
            curr = curr.next
        
        return res


    
    def __move_node_to_front(self, node: LRUNode[T]):
        if not self.__head:
            raise ValueError("Unsupported operation")
        
        # if this node is at tail
        if node.next is None:
            self.__tail = node.prev

        if node.prev is not None:
            node.prev.next = node.next

        node.next = self.__head
        node.prev = None
        self.__head.prev = node
        self.__head = node
            

    def get(self, key: str) -> T:
        if key not in self.__node_map or not self.__head:
            raise KeyError(f"Item with key {key} does not exists")

        target_node: LRUNode[T] = self.__node_map[key]
        self.__move_node_to_front(target_node)
        return target_node.value


    def get_or_default(self, key: str, default: Optional[T] = None) -> Optional[T]:
        try:
            return self.get(key=key)
        except KeyError:
            return default

    
    def insert(self, key: str, value: T):
        if key in self.__node_map:
            raise ValueError(f"key {key} already present")
        
        new_node = LRUNode(key=key, value=value)
        # Modifying linked list
        if self.__head is None:
            self.__head = new_node
            self.__tail = new_node
        else:
            new_node.next = self.__head
            self.__head.prev = new_node
            self.__head = new_node
        
        self.__node_map[key] = new_node
        
        # If cache size is full then removing the last item
        if self.size > self.max_size: 
            if self.__tail is not None and self.__tail.prev is not None:
                # removing from map
                del self.__node_map[self.__tail.key]

                self.__tail.prev.next = None
        


        
    def upsert(self, key: str, value: T) -> bool:
        try:
            self.insert(key=key, value=value)
            return True
        except ValueError:
            pass
        
        # Update logic
        target_node = self.__node_map[key]
        target_node.value = value

        # modify order
        self.__move_node_to_front(target_node)
        return False
    
    def delete(self, key: str) -> T:
        if key not in self.__node_map:
            raise KeyError(f"Item with key {key} does not exists")

        target_node = self.__node_map[key]
        if target_node.next is None and target_node.prev is None:
            # one and only node
            self.__head = None
            self.__tail = None
            self.__node_map = {}
            
        elif target_node.prev is None:
            # head node
            self.__head = target_node.next
            if self.__head:
                self.__head.prev = None
            
            del self.__node_map[key]
        
        elif target_node.next is None:
            # this is a tail node
            self.__tail = target_node.prev
            if self.__tail:
                self.__tail.next = None
            
            del self.__node_map[key]

        else:
            # It's a node in the middle
            target_node.prev.next = target_node.next
            del self.__node_map[key]
     
        return target_node.value


    def delete_or_default(self, key: str, default: Optional[T] = None) -> Optional[T]:
        try:
            return self.delete(key=key)
        except KeyError:
            return default
        
