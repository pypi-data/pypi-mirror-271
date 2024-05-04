import pkg_resources
from miml.data import Instance
from miml.data import Bag
from miml.data import MIMLDataset
from miml.data import load_dataset

dataset_test = load_dataset(pkg_resources.resource_filename('miml', 'datasets/miml_birds_random_80train.arff'),
                            delimiter="'")

dataset_test.show_dataset(head=5)
dataset_test.describe()

values = [2, 7, 5.09, 1, 0]
instance1 = Instance(values)
instance2 = Instance(values)
bag = Bag("bag1")
bag.add_instance(instance1)
bag.add_instance(instance2)
bag2 = Bag("bag2")
bag2.add_instance(instance2)

dataset = MIMLDataset()
dataset.set_features_name(["attr1", "attr2", "attr3"])
dataset.set_labels_name(["label1", "label2"])
# instance1.show_instance()
dataset.add_bag(bag)
dataset.add_bag(bag2)

dataset.show_dataset()
dataset.describe()
