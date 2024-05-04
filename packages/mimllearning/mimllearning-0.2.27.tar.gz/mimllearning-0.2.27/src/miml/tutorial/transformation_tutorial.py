import pkg_resources
from miml.data import load_dataset
from miml.transformation import ArithmeticTransformation, BinaryRelevanceTransformation

dataset_test = load_dataset(pkg_resources.resource_filename('miml', 'datasets/miml_birds_random_20test.arff'),
                            delimiter="'")

# TODO: Use a smaller dataset and convert to ipnyb to see results easily

transformed_ml_dateset_x, transformed_ml_dateset_y = ArithmeticTransformation().transform_dataset(dataset_test)
# We get two numpy.ndarrays, first with feature values and other with labels
print(transformed_ml_dateset_x[:5, ], transformed_ml_dateset_y[:5])

transformed_mi_datasets = BinaryRelevanceTransformation().transform_dataset(dataset_test)
# we get n_labels datasets with two numpy.ndarrays, first with feature values and other with values of one label
for dataset in transformed_mi_datasets:
    print(dataset[0][:5, ], dataset[1][:5])
