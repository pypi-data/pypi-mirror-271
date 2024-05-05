
import numpy as np

from .miml_to_ml_transformation import MIMLtoMLTransformation
from ...data import Instance
from ...data import Bag
from ...data import MIMLDataset


class GeometricTransformation(MIMLtoMLTransformation):
    """
    Class that performs a geometric transformation to convert a MIMLDataset class to numpy ndarrays.
    """

    def __init__(self):
        super().__init__()

    def transform_dataset(self, dataset: MIMLDataset) -> MIMLDataset:
        """
        Transform the dataset to multilabel dataset converting each bag into a single instance being the value of each
        attribute the geometric center of the instances in the bag.

        Returns
        -------
        """
        self.dataset = dataset
        transformed_dataset = MIMLDataset()
        transformed_dataset.set_name(dataset.get_name())
        transformed_dataset.set_features_name(dataset.get_features_name())
        transformed_dataset.set_labels_name(dataset.get_labels_name())
        for bag_index, key in enumerate(self.dataset.data.keys()):
            transformed_bag = self.transform_bag(self.dataset.get_bag(key))
            transformed_dataset.add_bag(transformed_bag)

        return transformed_dataset

    def transform_bag(self, bag: Bag) -> Bag:
        """
        Transform a bag to a multilabel instance

        Parameters
        ----------
        bag : Bag
            Bag to be transformed to multilabel instance

        Returns
        -------
        features : ndarray of shape (n_features)
            Numpy array with feature values

        labels : ndarray of shape (n_labels)
            Numpy array with label values
        """
        # TODO: Test

        features = bag.get_features()
        labels = bag.get_labels()[0]
        min_values = np.min(features, axis=0)
        max_values = np.max(features, axis=0)
        features = (min_values + max_values) / 2
        transformed_bag = Bag(bag.key)
        transformed_bag.add_instance(Instance(list(np.hstack((features, labels)))))
        return transformed_bag
