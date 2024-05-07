import mil.models
import numpy as np


class APRClassifier:
    """
    Approach is to construct an APR by starting with
    a single positive instance and “growing” the APR by expanding it to cover additional
    positive instances.
    We call it the “iterated discrimination” algorithm, and it has three basic procedures:
    -Grow. An algorithm for growing an APR with “tight” bounds along a specified set
    of features.
    -Discrim. An algorithm for choosing a set of discriminating features by analyzing
    an APR.
    -Expand. An algorithm for expanding the bounds of an APR to improve its generalization ability.

    Attributes
    ----------
    classifier
        Classifier used from mil library

    References
    ----------
    Thomas G. Dietterich, Richard H. Lathrop, Tomas Lozano-Perez "Solving the multiple instance problem
    with axis-parallel rectangles" 1997
    Model implementation https://github.com/rosasalberto/mil/blob/master/mil/models/instance_level/apr.py
    Matlab implementation https://github.com/DMJTax/mil
    """

    def __init__(self) -> None:
        """
        Constructor of the class APRClassifier
        """
        self.classifier = mil.models.APR(verbose=0)

    def fit(self, x_train, y_train) -> None:
        """
        Fit the classifier to the training data.

        Parameters
        ----------
        x_train : ndarray of shape (n_bags, n_instances, n_features)
            Features values of bags in the training set.
        y_train : ndarray (n_bags, n_instances, n_labels)
            Labels of bags in the training set.
        """
        self.classifier.fit(x_train, y_train)

    def predict(self, x) -> int:
        """
        Predict the label of the bag

        Parameters
        ----------
        x: np.ndarray of shape(n_instances, n_features)
            features values of a bag

        Returns
        -------
        label: int
            Predicted label of the bag
        """
        # TODO: Revisar dimensiones de x, que pasa si llamo a predict con varias bolsas
        x = x.reshape(1, x.shape[0], x.shape[1])
        return self.classifier.predict(x)

    def predict_proba(self, x: np.ndarray):
        result = np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            result[i] = self.predict(x[i])
        return result
