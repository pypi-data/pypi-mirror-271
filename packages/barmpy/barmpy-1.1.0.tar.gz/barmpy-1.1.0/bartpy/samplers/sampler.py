from abc import abstractmethod, ABC

from barmpy.model import Model
from barmpy.tree import Tree


class Sampler(ABC):

    @abstractmethod
    def step(self, model: Model, tree: Tree) -> bool:
        raise NotImplementedError()
