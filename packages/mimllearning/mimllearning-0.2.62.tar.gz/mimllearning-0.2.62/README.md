# miml: Multi Instance Multi Label Learning Library for Python
The aim of the library is to ease the development, testing and comparison of classification algorithms for multi-instance multi-label learning (MIML). 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install miml.

```bash
$ pip install mimllearning
```
#### Requirements
The requirement packages for miml library are: numpy, scikit-learn, scipy, mil, tensorflow and keras.
Installing miml with the package manager does not install the package dependencies.
So install them with the package manager manually if not already downloaded.

    $ pip install numpy
    $ pip install scikit-learn
    $ pip install scipy
    $ pip install mil
    $ pip install tensorflow
    $ pip install keras==2.12.0

### Usage


#### Datasets

``` python
import pkg_resources
from miml.data.load_datasets import load_dataset

dataset_train = load_dataset(pkg_resources.resource_filename('miml', 'datasets/miml_birds_random_80train.arff'),
                             delimiter="'")
dataset_test = load_dataset(pkg_resources.resource_filename('miml', 'datasets/miml_birds_random_20test.arff'),
                            delimiter="'")
```

#### Classifier

``` python
from miml.classifier import MIMLtoMIBRClassifier, AllPositiveAPRClassifier

classifier_mi = MIMLtoMIBRClassifier(AllPositiveAPRClassifier())
classifier_mi.fit(dataset_train)
results_mi=classifier_mi.evaluate(dataset_test)
```

#### Report

``` python
from miml.report import Report

report = Report()
report.to_string(dataset_test.get_labels_by_bag(), results_ml)
print("")
report.to_csv(dataset_test.get_labels_by_bag(), results_ml)
```

### License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
- **[MIT license](http://opensource.org/licenses/mit-license.php)**