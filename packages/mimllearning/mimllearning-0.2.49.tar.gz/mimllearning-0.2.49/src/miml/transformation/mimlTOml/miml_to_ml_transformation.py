from abc import ABC, abstractmethod
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMLTransformation(ABC):

    def __init__(self) -> None:
        self.dataset = None

    @abstractmethod
    def transform_dataset(self, dataset: MIMLDataset) -> MIMLDataset:
        pass

    @abstractmethod
    def transform_bag(self, bag: Bag) -> Bag:
        pass

