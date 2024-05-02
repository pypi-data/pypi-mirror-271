
import numpy as np

from .miml_to_ml_transformation import MIMLtoMLTransformation
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
        x = np.empty(shape=(self.dataset.get_number_bags(), self.dataset.get_number_features() * 2))
        y = np.empty(shape=(self.dataset.get_number_bags(), self.dataset.get_number_labels()))
        for bag_index, key in enumerate(self.dataset.data.keys()):
            features, labels = self.transform_bag(self.dataset.get_bag(key))
            x[bag_index] = features
            y[bag_index] = labels

        return x, y

    def transform_bag(self, bag: Bag):
        """
        Transform a bag to a multilabel instance

        Parameters
        ----------
        bag : Bag
            Bag to be transformed to multilabel instance

        Returns
        -------
        features : ndarray of shape (n_features*2)
            Numpy array with feature values

        labels : ndarray of shape (n_labels)
            Numpy array with label values
        """
        features = bag.get_features()
        labels = bag.get_labels()[0]
        min_values = np.min(features, axis=0)
        max_values = np.max(features, axis=0)
        features = np.concatenate((min_values, max_values), axis=0)

        return features, labels
