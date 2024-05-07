
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
        features_name_min = ["min_" + feature for feature in features_name]
        features_name_max = ["max_" + feature for feature in features_name]
        transformed_dataset.set_features_name(features_name_min+features_name_max)
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
        if bag.dataset is None:
            raise Exception("Can't transform a bag without an assigned dataset, because we wouldn't have info about "
                            "the features and labels")

        features = bag.get_features()
        labels = bag.get_labels()[0]
        min_values = np.min(features, axis=0)
        max_values = np.max(features, axis=0)
        features = np.concatenate((min_values, max_values), axis=0)
        transformed_bag = Bag(bag.key)
        transformed_bag.add_instance(Instance(list(np.hstack((features, labels)))))

        dataset = MIMLDataset()
        dataset.set_name(bag.dataset.get_name())
        features_name = self.dataset.get_features_name()
        features_name_min = ["min_" + feature for feature in features_name]
        features_name_max = ["max_" + feature for feature in features_name]
        dataset.set_features_name(features_name_min+features_name_max)
        dataset.set_labels_name(bag.dataset.get_labels_name())
        dataset.add_bag(transformed_bag)

        return transformed_bag

