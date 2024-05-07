import numpy as np
from copy import deepcopy

from .miml_to_mi_classifier import MIMLtoMIClassifier
from ...transformation import BinaryRelevanceTransformation
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMIBRClassifier(MIMLtoMIClassifier):
    """
    Class to represent a multiinstance classifier
    """

    def __init__(self, classifier) -> None:
        """
        Constructor of the class MIMLtoMIBRClassifier

        Parameters
        ----------
        classifier
            Specific classifier to be used
        """
        super().__init__(classifier)
        self.transformation = BinaryRelevanceTransformation()
        self.classifiers = []

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """
        for x in range(dataset_train.get_number_labels()):
            classifier = deepcopy(self.classifier)
            self.classifiers.append(classifier)

        datasets = self.transformation.transform_dataset(dataset_train)
        for i, dataset in enumerate(datasets):
            self.classifiers[i].fit(dataset.get_features_by_bag(), dataset.get_labels_by_bag())

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict labels of given data

        Parameters
        ----------
        x : ndarray of shape (n_instances, n_labels)
            Data to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels
        """
        results = np.zeros((len(self.classifiers)))
        # Prediction of each label
        for i in range(len(self.classifiers)):
            results[i] = self.classifiers[i].predict(x)
        return results

    def predict_bag(self, bag: Bag) -> np.ndarray:
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels of the bag
        """
        # super().predict_bag(bag)

        bags = self.transformation.transform_bag(bag)

        return self.predict(bags[0].get_features())

    def predict_proba(self, dataset_test: MIMLDataset):
        # TODO: DOC
        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        datasets = self.transformation.transform_dataset(dataset_test)

        for i in range(len(datasets)):
            results[0:, i] = self.classifiers[i].predict_proba(datasets[i].get_features_by_bag())
        return results

    def evaluate(self, dataset_test: MIMLDataset) -> np.ndarray:
        """
        Evaluate the model on a test dataset

        Parameters
        ----------
        dataset_test : MIMLDataset
            Test dataset to evaluate the model on

        Returns
        ----------
        results : ndarray of shape (n_bags, n_labels)
            Predicted labels of dataset_test
        """
        # super().evaluate(dataset_test)

        datasets = self.transformation.transform_dataset(dataset_test)

        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        # Features are the same in all datasets
        for i, bag in enumerate(datasets[0].get_features_by_bag()):
            results[i] = self.predict(bag)

        return results
