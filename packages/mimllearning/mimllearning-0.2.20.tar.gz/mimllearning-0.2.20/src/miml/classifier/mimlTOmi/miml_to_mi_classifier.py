import numpy as np
from abc import abstractmethod
from ..miml_classifier import MIMLClassifier
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMIClassifier(MIMLClassifier):
    """
    Class to represent a multiinstance classifier
    """

    def __init__(self, mi_classifier):
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
    def fit_internal(self, dataset_train: MIMLDataset):
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """
        pass

    @abstractmethod
    def predict(self, x: np.ndarray):
        """
        Predict labels of given data

        Parameters
        ----------
        x : ndarray of shape (n, n_labels)
            Data to predict their labels
        """
        pass

    @abstractmethod
    def predict_bag(self, bag: Bag):
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels
        """
        pass

    @abstractmethod
    def evaluate(self, dataset_test: MIMLDataset):
        """
        Evaluate the model on a test dataset

        Parameters
        ----------
        dataset_test : MIMLDataset
            Test dataset to evaluate the model on
        """
        pass
