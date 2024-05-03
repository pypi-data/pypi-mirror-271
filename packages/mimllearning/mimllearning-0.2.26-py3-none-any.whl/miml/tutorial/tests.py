from sklearn.neighbors import KNeighborsClassifier

from miml.classifier import MIMLtoMLClassifier, MIMLtoMIBRClassifier, AllPositiveAPRClassifier, IteratedDiscrimAPRClassifier
from miml.data import load_dataset
from miml.transformation import ArithmeticTransformation

dataset_train = load_dataset("../datasets/miml_birds_random_80train.arff", delimiter="'")
dataset_test = load_dataset("../datasets/miml_birds_random_20test.arff", delimiter="'")

classifier_mi = MIMLtoMIBRClassifier(AllPositiveAPRClassifier())
classifier_mi.fit(dataset_train)
classifier_mi.evaluate(dataset_test)

classifier_mi = MIMLtoMIBRClassifier(IteratedDiscrimAPRClassifier())
classifier_mi.fit(dataset_train)
classifier_mi.evaluate(dataset_test)
