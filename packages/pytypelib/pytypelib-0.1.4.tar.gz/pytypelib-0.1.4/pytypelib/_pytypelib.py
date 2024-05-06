from typing import (TypeVar, overload, MutableMapping, List,
    Dict, Any, Iterator, runtime_checkable, Protocol, final)
from collections import defaultdict
from copy import deepcopy

K = TypeVar("K") #K (key or list type)
V = TypeVar("V") #V (value or dict type)

@runtime_checkable
class _Proto(Protocol):
    def __init__(self, data) -> Any|None: ...

class _ProtoMap(MutableMapping[K, V], _Proto):
    data: List[K] | Dict[K, V]
    @overload
    def __init__(self, data: None = None, /) -> None: ...
    @overload
    def __init__(self, data: List = [K], /) -> Dict: ...
    @overload
    def __init__(self, data: Dict = {K: V}) -> Dict: ...
    @overload
    def __init__(self, data: List|Dict) -> Any: ...
    def __getitem__(self, key: K) -> V: ...
    def __setitem__(self, key: K, value: V) -> None: ...
    def __delitem__(self, key: K) -> None: ...
    def __iter__(self) -> Iterator[K]: ...
    def __len__(self) -> int: ...
    def __getattribute__(self, name: str) -> K: ...
    def __repr__(self) -> K: ...

class PlaceMap(_ProtoMap[K, V]):
    """Create map of data that is given, in relation to keys and their placement\n
    if 'data' value is List, PlaceMap returns a dict:
    ```python
        >>> data = ['a', 'b', 'c']
        >>> dpm = PlaceMap(data)
        >>> print(dmp)
        {0:'a', 1:'b', 2:'c'}
    ```
    if 'data' is Dict, PlaceMap does the opposite process, returning a list:
    ```python
        >>> data = {0:'a', 1:'b', 2:'c'}
        >>> lpm = PlaceMap(data)
        >>> print(lmp)
        ['a', 'b', 'c']
    """
    
    def __init__(self, data) -> Any:
        self._data: Dict|List = data
        if isinstance(data, List):
            self._fdat = defaultdict(lambda: None)
            self._final = {}
            self._cache = {} #cache section
            for key, val in enumerate(data):
                self._fdat[key] = val
            self._final = dict(self._fdat)
            self._cache = dict(self._fdat)
        elif isinstance(data, Dict): 
            self._fdat = []
            self._final = []
            self._cache = [] #cache section
            _k = []
            clone = deepcopy(data)
            for key, val in clone.items():
                _k.append(key)
            _k.sort()
            for i in _k:
                self._fdat.append(clone[i])
            self._final = list(self._fdat)
            self._cache = list(self._fdat)
        else:
            raise TypeError("'data' type can only be 'dict' or 'list'")

    def __getitem__(self, key: K) -> V:
        return self._final[key]

    def __setitem__(self, key: K, value: V) -> None:
        self._final[key] = value

    def __delitem__(self, key: K) -> None:
        del self._final[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._final)
        """
        if isinstance(self._data, List):
            return iter(dict(self._final))
        if isinstance(self._data, Dict):
            return iter(list(self._final))
        """

    def __len__(self) -> int:
        return len(self._final)

    def __getattribute__(self, name: str) -> K|V:
        attrs = ("_fdat", "_final", "_data", "get_unmap", "get_remap", "unmap", "remap", "_cache", "__dict__")
        if name in attrs:
            return object.__getattribute__(self, name)
        else:
            return getattr(self._final, name)
        
    def __str__(self) -> str:
        return str(self._final)
    
    def __repr__(self) -> str:
        return repr(self._final)
    
    @final
    @property
    def get_unmap(self) -> K:
        "get original data without converting it back"
        return self._data
    
    @final
    def unmap(self) -> K:
        """returns the data back to the original"""
        self._final = self._data

    @final
    def remap(self) -> V:
        """used if you want to return an unmapped value to the PlaceMap value"""
        if isinstance(self._data, List):
            if isinstance(self._final, List):
                self._final = self._cache
        elif isinstance(self._data, Dict):
            if isinstance(self._final, Dict):
                self._final = self._cache
    
    @final
    @property
    def get_remap(self) -> V:
        """returns remap value without performing remap on original data"""
        return self._cache