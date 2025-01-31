from collections import namedtuple
from enum import Enum, auto

Coordinate = namedtuple('Coordinate', ['x', 'y'])

class AgentType(Enum):
    RED = auto()
    BLUE = auto()
    BLACK = auto()
    INNOCENT = auto()



