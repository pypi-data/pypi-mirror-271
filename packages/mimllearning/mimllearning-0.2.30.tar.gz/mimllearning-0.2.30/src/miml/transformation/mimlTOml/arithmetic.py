
import numpy as np

from .miml_to_ml_transformation import MIMLtoMLTransformation
from ...data import Instance
from ...data import Bag
from ...data import MIMLDataset


class ArithmeticTransformation(MIMLtoMLTransformation):
    """
    Class that performs an arithmetic transformation to convert a MIMLDataset class to numpy ndarrays.
    """

    def __init__(self):
        super().__init__()

    def transform_dataset(self, dataset: MIMLDataset) -> MIMLDataset:
        """
        Transform the dataset to multilabel dataset converting each bag into a single instance being the value of each
        attribute the mean value of the instances in the bag.

        Parameters

        Returns
        -------

        X : ndarray of shape (n_bags, n_features)
            Training vector

        Y : ndarray of shape (n_bags, n_labels)
            Target vector relative to X.
        """
        self.dataset = dataset
        transformed_dataset = MIMLDataset()
        transformed_dataset.set_name(dataset.get_name())
        transformed_dataset.set_features_name(dataset.get_features_name())
        transformed_dataset.set_labels_name(dataset.get_labels_name())
        for bag_index, key in enumerate(self.dataset.data.keys()):
            features, labels = self.transform_bag(self.dataset.get_bag(key))
            bag = Bag(key)
            bag.add_instance(Instance(features+labels))
            transformed_dataset.add_bag(bag)

        return transformed_dataset

    def transform_bag(self, bag: Bag):
        """
        Transform a bag to a multilabel instance

        Parameters
        ----------
        bag : Bag
            Key of the bag to be transformed

        Returns
        -------
        features : ndarray of shape (n_features)
            Numpy array with feature values

        labels : ndarray of shape (n_labels)
            Numpy array with label values
        """

        features = bag.get_features()
        labels = bag.get_labels()[0]
        features = np.mean(features, axis=0)
        return features, labels
