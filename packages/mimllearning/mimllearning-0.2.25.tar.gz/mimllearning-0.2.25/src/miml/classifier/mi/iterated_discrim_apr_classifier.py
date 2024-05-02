import numpy as np


class IteratedDiscrimAPRClassifier:

    def __init__(self):
        """

        """
        # self.classifier = mil.models.APR(step=10, verbose=0)
        self.apr = []
        self.positive_bag_indices = None
        self.x_train = None
        self.y_train = None

    def fit(self, x_train, y_train):
        """

        Parameters
        ----------
        x_train
        y_train
        """
        self.x_train = x_train
        self.y_train = y_train
        self.generate_apr()
        # for _ in range(3):
        self.grow()
        #    self.discriminate()

    def predict(self, bag: np.array) -> int:
        """
        Predict the label of the bag

        Parameters
        ----------
        bag: np.ndarray of shape(n_instances, n_features)
            features values of a bag

        Returns
        -------
        label: int
            Predicted label of the bag

        """
        if np.all(bag >= self.apr[0]):
            if np.all(bag <= self.apr[1]):
                return 1
        return 0

    def generate_apr(self):

        self.positive_bag_indices = np.where(self.y_train == 1)[0]

        initial_bag_index = np.random.choice(self.positive_bag_indices)
        initial_index_instance = np.random.choice(self.x_train[initial_bag_index].shape[0])
        apr_min = apr_max = self.x_train[initial_bag_index][initial_index_instance]

        self.apr = [apr_min, apr_max]

    def grow(self):

        while True:
            not_positives_bag_in_apr = []

            for bag_index in self.positive_bag_indices:
                for instance in self.x_train[bag_index]:
                    if np.all(instance >= self.apr[0]) and np.all(instance <= self.apr[1]):
                        # There is already an instance of the bag in apr
                        break
                else:
                    # If any instance in apr we need to get one of the bag
                    not_positives_bag_in_apr.append(bag_index)

            if not not_positives_bag_in_apr:
                return

            # calculate new apr with not_positive_bag_in_apr and compare size
            new_aprs = []
            new_aprs_size = []

            for bag_index in not_positives_bag_in_apr:
                for instance in self.x_train[bag_index]:
                    apr_min = np.minimum(self.apr[0], instance)
                    apr_max = np.maximum(self.apr[1], instance)
                    apr = (apr_min, apr_max)
                    new_aprs.append(apr)
                    new_aprs_size.append(self.size(apr))

            # actualizamos nuestro apr
            self.apr = new_aprs[new_aprs_size.index(min(new_aprs_size))]

    def discriminate(self, margin=0.1):
        selected_features = []
        negative_bag_indices = np.where(self.y_train == 0)[0]
        while negative_bag_indices:
            discrimination_counts = np.zeros(self.x_train.shape[1])

            for bag_index in negative_bag_indices:
                for instance in self.x_train[bag_index]:
                    for feature_index in range(self.x_train.shape[1]):
                        if (instance[feature_index] < self.apr[0][feature_index] - margin or
                                instance[feature_index] > self.apr[1][feature_index] + margin):
                            discrimination_counts[feature_index] += 1

            if not np.any(discrimination_counts):
                break

            max_discrimination_feature = np.argmax(discrimination_counts)
            selected_features.append(max_discrimination_feature)

            # Remove instances strongly discriminated by the selected feature
            new_negative_instances_indices = []
            for bag_index in negative_bag_indices:
                for instance in self.x_train[bag_index]:
                    if (instance[max_discrimination_feature] < self.apr[0][max_discrimination_feature] - margin or
                            instance[max_discrimination_feature] > self.apr[1][max_discrimination_feature] + margin):
                        pass
                        # new_negative_instances_indices.append(instance_index)
            negative_instances_indices = new_negative_instances_indices

        return selected_features

    def size(self, apr):
        size = 0
        for i in range(self.apr[0].shape[0]):
            size += apr[1][i] - apr[0][i]
        return size
