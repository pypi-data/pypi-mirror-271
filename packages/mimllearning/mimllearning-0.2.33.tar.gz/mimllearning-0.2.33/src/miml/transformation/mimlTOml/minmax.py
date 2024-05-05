
import numpy as np

from .miml_to_ml_transformation import MIMLtoMLTransformation
from ...data import Instance
from ...data import Bag
from ...data import MIMLDataset


class MinMaxTransformation(MIMLtoMLTransformation):
    """
    Class that performs a minmax transformation to convert a MIMLDataset class to numpy ndarrays.
    """

    def __init__(self):
        super().__init__()

    def transform_dataset(self, dataset: MIMLDataset):
        """
        Transform the dataset to multilabel dataset converting each bag into a single instance with the min and max
        value of each attribute as two new attributes.

        Returns
        -------

        X : ndarray of shape (n_bags, n_features*2)
            Training vector

        Y : ndarray of shape (n_bags, n_labels)
            Target vector relative to X.

        """
        self.dataset = dataset
        transformed_dataset = MIMLDataset()
        transformed_dataset.set_name(dataset.get_name())
        features_name = dataset.get_features_name()
        features_name_minmax = features_name
        for index, feature in enumerate(features_name):
            features_name_minmax[index] = "min_" + feature
            features_name.append("max_"+feature)
        transformed_dataset.set_features_name(features_name_minmax)
        transformed_dataset.set_labels_name(dataset.get_labels_name())
        for bag_index, key in enumerate(self.dataset.data.keys()):
            transformed_bag = self.transform_bag(self.dataset.get_bag(key))
            transformed_dataset.add_bag(transformed_bag)

        return transformed_dataset

    def transform_bag(self, bag: Bag):
        """
        Transform a bag to a multilabel instance

        Parameters
        ----------
        bag : Bag
            Bag to be transformed to multilabel instance

        Returns
        -------
        transformed_bag : Bag
            Transformed bag

        """
        features = bag.get_features()
        labels = bag.get_labels()[0]
        min_values = np.min(features, axis=0)
        max_values = np.max(features, axis=0)
        features = np.concatenate((min_values, max_values), axis=0)
        transformed_bag = Bag(bag.key)
        transformed_bag.add_instance(Instance(list(np.hstack((features, labels)))))
        return transformed_bag

