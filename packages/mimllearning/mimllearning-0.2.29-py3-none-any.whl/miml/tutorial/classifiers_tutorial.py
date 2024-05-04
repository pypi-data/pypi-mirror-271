import pkg_resources

from sklearn.neighbors import KNeighborsClassifier
from miml.classifier import MIMLtoMLClassifier, MIMLtoMIBRClassifier, AllPositiveAPRClassifier
from miml.data import load_dataset
from miml.transformation import ArithmeticTransformation
from miml.report import Report


dataset_train = load_dataset(pkg_resources.resource_filename('miml', 'datasets/miml_birds_random_80train.arff'),
                             delimiter="'")
dataset_test = load_dataset(pkg_resources.resource_filename('miml', 'datasets/miml_birds_random_20test.arff'),
                            delimiter="'")

report = Report()

classifier_ml = MIMLtoMLClassifier(KNeighborsClassifier(), ArithmeticTransformation())
classifier_ml.fit(dataset_train)
print(classifier_ml.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])
results = classifier_ml.evaluate(dataset_test)
report.to_string(dataset_test.get_labels_by_bag(), results)
report.to_csv(dataset_test.get_labels_by_bag(), results)


classifier_mi = MIMLtoMIBRClassifier(AllPositiveAPRClassifier())
classifier_mi.fit(dataset_train)
print(classifier_mi.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])
classifier_mi.evaluate(dataset_test)
