import numpy as np
from ...data import MIMLDataset
from ...data import Bag
from ..miml_classifier import MIMLClassifier
from ...transformation.mimlTOml.miml_to_ml_transformation import MIMLtoMLTransformation


class MIMLtoMLClassifier(MIMLClassifier):

    def __init__(self, ml_classifier, transformation: MIMLtoMLTransformation) -> None:
        """
        Constructor of the class MIMLtoMIClassifier

        Parameters
        ----------
        ml_classifier
            Specific classifier to be used

        transformation : MIMLtoMLTransformation
            Transformation to be used
        """
        super().__init__()
        self.classifier = ml_classifier
        self.transformation = transformation

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train : MIMLDataset
            Dataset to train the classifier
        """
        transformed_dataset_train = self.transformation.transform_dataset(dataset_train)
        self.classifier.fit(transformed_dataset_train.get_features(), transformed_dataset_train.get_labels())

    def predict(self, x: np.ndarray):
        """
         Predict labels of given data

         Parameters
         ----------
         x : ndarray of shape (n, n_labels)
             Data to predict their labels
         """
        return self.classifier.predict(x)

    def predict_bag(self, bag: Bag) -> np.ndarray:
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels
        """
        # TODO: Check number attributes of bag with dataset
        # super().predict_bag(bag)
        x_bag, _ = self.transformation.transform_bag(bag)
        x_bag = np.array(x_bag, ndmin=2)
        return self.predict(x_bag)

    def evaluate(self, dataset_test: MIMLDataset):
        """
        Evaluate the model on a test dataset

        Parameters
        ----------
        dataset_test : MIMLDataset
            Test dataset to evaluate the model on.
        """
        # super().evaluate(dataset_test)
        transformed_dataset_test = self.transformation.transform_dataset(dataset_test)
        results = self.predict(transformed_dataset_test.get_features())

        return results
