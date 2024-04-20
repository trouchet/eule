from typing import Union, List, Dict, Tuple, Set

KeyType = Union[str, Tuple]
SetType = Union[List, Set]
SetsType = Union[List[SetType], Dict[KeyType, SetType]]
PseudoSequenceType = Union[str, List, Tuple]
SequenceType = Union[List, Tuple, Set]