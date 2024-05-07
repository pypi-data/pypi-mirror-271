
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
        transformed_dataset : MIMLDataset
            Transformed dataset

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

    def transform_bag(self, bag: Bag):
        """
        Transform a bag to a multilabel instance

        Parameters
        ----------
        bag : Bag
            Bag to be transformed

        Returns
        -------
        """
        if bag.dataset is None:
            raise Exception("Can't transform a bag without an assigned dataset, because we wouldn't have info about "
                            "the features and labels")

        features = bag.get_features()
        labels = bag.get_labels()[0]
        features = np.mean(features, axis=0)

        transformed_bag = Bag(bag.key)
        transformed_bag.add_instance(Instance(list(np.hstack((features, labels)))))

        dataset = MIMLDataset()
        dataset.set_name(bag.dataset.get_name())
        dataset.set_features_name(bag.dataset.get_features_name())
        dataset.set_labels_name(bag.dataset.get_labels_name())
        dataset.add_bag(transformed_bag)

        return transformed_bag
