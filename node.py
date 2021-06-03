import copy
from dataclasses import dataclass, field
from typing import List

@dataclass
class Node:
  '''
  Node Structure
  '''

  station: str
  connections: List[str]
  path_so_far: List[str] = field(default_factory=lambda: [])
  real_cost_so_far: float = 0.0
  estimate_cost: float = 0.0
  parent: str = ""