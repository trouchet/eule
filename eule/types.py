from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

KeyType = str | Tuple
SetType = List | Set
SetsType = List[SetType] | Dict[KeyType, SetType]
PseudoSequenceType = str | List | Tuple
SequenceType = List | Tuple | Set
