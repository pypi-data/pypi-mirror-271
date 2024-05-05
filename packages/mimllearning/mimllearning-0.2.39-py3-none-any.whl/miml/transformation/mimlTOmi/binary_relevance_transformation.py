from copy import deepcopy

from ...data import Bag
from ...data import MIMLDataset


class BinaryRelevanceTransformation:
    """
    Class that performs a binary relevance transformation to convert a MIMLDataset class to numpy ndarrays.
    """

    def __init__(self):
        self.dataset = None

    def transform_dataset(self, dataset: MIMLDataset) -> list:
        """
        Transform the dataset to multiinstance datasets dividing the original dataset into n datasets with a single
        label, where n is the number of labels.

        Returns
        -------

        datasets: list
            Multi instance datasets

        """
        self.dataset = dataset
        datasets = []

        for i in range(self.dataset.get_number_labels()):
            dataset = deepcopy(self.dataset)
            count = 0
            for j in range(self.dataset.get_number_labels()):
                if i != j:
                    dataset.delete_attribute(self.dataset.get_number_features()-count+j)
                    count += 1
            datasets.append(dataset)

        return datasets

    def transform_bag(self, bag: Bag) -> list:
        """
        Transform miml bag to multi instance bags

        Parameters
        ----------
        bag :
            Bag to be transformed to multiinstance bag

        Returns
        -------
        bags : list[ndarray]
        Tuple of numpy ndarray with attribute values and labels

        """
        bags = [[bag.get_features(), label] for label in bag.get_labels()[0]]
        return bags
