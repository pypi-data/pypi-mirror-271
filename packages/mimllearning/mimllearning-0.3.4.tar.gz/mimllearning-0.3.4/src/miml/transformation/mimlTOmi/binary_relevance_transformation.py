import numpy as np
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
                    labels_name = dataset.get_labels_name()
                    labels_name.pop(j-count)
                    dataset.set_labels_name(labels_name)
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
        bags : list[Bag]
            List of n_labels transformed bags

        """
        if bag.dataset is None:
            raise Exception("Can't transform a bag without an assigned dataset, because we wouldn't have info about "
                            "the features and labels")

        bags = []
        for i in range(bag.get_number_labels()):
            transformed_bag = deepcopy(bag)
            count = 0
            for j in range(bag.get_number_labels()):
                if i != j:
                    transformed_bag.data = np.delete(transformed_bag.data, bag.get_number_features() - count + j, axis=1)
                    labels_name = transformed_bag.dataset.get_labels_name()
                    labels_name.pop(j - count)
                    transformed_bag.dataset.set_labels_name(labels_name)
                    count += 1
            bags.append(transformed_bag)

        return bags
