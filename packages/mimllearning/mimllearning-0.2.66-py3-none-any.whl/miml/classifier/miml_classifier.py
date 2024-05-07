import numpy as np
from abc import ABC, abstractmethod

from ..data import Bag
from ..data import MIMLDataset


class MIMLClassifier(ABC):
    """
    Class to represent a MIMLClassifier
    """

    def __init__(self) -> None:
        """
        Constructor of the class MIMLClassifier
        """
        self.classifier = None

    def fit(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train : MIMLDataset
            Dataset to train the classifier
        """
        # if not isinstance(dataset_train, MIMLDataset):
        #    raise Exception("Fit function should receive a MIMLDataset as parameter")

        self.fit_internal(dataset_train)

    @abstractmethod
    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Internal method to train the classifier

        Parameters
        ----------
        dataset_train : MIMLDataset
            Dataset to train the classifier
        """
        pass

    @abstractmethod
    def predict(self, x: np.ndarray) -> np.ndarray:
        """
         Predict labels of given data

         Parameters
         ----------
         x : ndarray of shape (n, n_labels)
             Data to predict their labels

        Returns
        ----------
        results : ndarray of shape (n_bags, n_labels)
            Predicted labels of data
        """
        # if not isinstance(x, np.ndarray):
        #    raise Exception("Predict function should receive a Numpy array as parameter")

    @abstractmethod
    def predict_bag(self, bag: Bag) -> np.ndarray:
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels

        Returns
        ----------
        results : ndarray of shape (n_bags, n_labels)
            Predicted labels of the bag
        """
        # if not isinstance(bag, Bag):
        #    raise Exception("Predict function should receive a Numpy array as parameter")

    @abstractmethod
    def predict_proba(self, dataset_test: MIMLDataset) -> np.ndarray:
        # TODO: DOC
        pass

    @abstractmethod
    def evaluate(self, dataset_test: MIMLDataset) -> np.ndarray:
        """
        Evaluate the model on a test dataset

        Parameters
        ----------
        dataset_test : MIMLDataset
            Test dataset to evaluate the model on.

        Returns
        ----------
        results : ndarray of shape (n_bags, n_labels)
            Predicted labels of dataset_test
        """
        # if not isinstance(dataset_test, MIMLDataset):
        #    raise Exception("Evaluate function should receive a MIMLDataset as parameter")
