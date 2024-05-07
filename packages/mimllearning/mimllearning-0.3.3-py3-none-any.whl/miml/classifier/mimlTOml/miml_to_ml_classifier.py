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

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
         Predict labels of given data

         Parameters
         ----------
         x : ndarray of shape (n_instances, n_labels)
             Data to predict their labels

         Returns
         ----------
         results : ndarray of shape (n_instances, n_labels)
             Predicted labels of data
         """
        return self.classifier.predict(x)

    def predict_bag(self, bag: Bag) -> np.ndarray:
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels

        Returns
         ----------
         results : ndarray of shape (n_labels)
             Predicted labels of data
        """

        # TODO: La bag por parametro tambien tiene que tener un dataset asociada para coger las features,
        # sino no se puede predecir. Mostrar error
        transformed_bag = self.transformation.transform_bag(bag)

        return self.predict(transformed_bag.get_features())

    def predict_proba(self, dataset_test: MIMLDataset) -> np.ndarray:
        # TODO: DOC
        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        transformed_dataset_test = self.transformation.transform_dataset(dataset_test)
        probs = self.classifier.predict_proba(transformed_dataset_test.get_features())
        for i, label in enumerate(probs):
            # It takes the probability of being a positive class
            results[0:, i] = label[0:, 1]
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
        transformed_dataset_test = self.transformation.transform_dataset(dataset_test)
        results = self.predict(transformed_dataset_test.get_features())

        return results
