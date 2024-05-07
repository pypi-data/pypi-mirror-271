import numpy as np
from abc import abstractmethod
from ..miml_classifier import MIMLClassifier
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMIClassifier(MIMLClassifier):
    """
    Class to represent a multiinstance classifier
    """

    def __init__(self, mi_classifier) -> None:
        """
        Constructor of the class MIMLtoMIClassifier

        Parameters
        ----------
        mi_classifier
            Specific classifier to be used
        """
        super().__init__()
        self.classifier = mi_classifier

    @abstractmethod
    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def predict_proba(self, dataset_test: MIMLDataset):
        """

        """
        pass

    @abstractmethod
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
        pass
