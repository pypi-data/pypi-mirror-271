import warnings
from sklearn.metrics import hamming_loss, accuracy_score, fbeta_score, jaccard_score, log_loss, \
    roc_auc_score, f1_score, precision_score, recall_score, average_precision_score
from ..classifier import MIMLClassifier
from ..data import MIMLDataset


class Report:
    """
    Class to generate a report
    """

    def __init__(self, classifier: MIMLClassifier, dataset_test: MIMLDataset, metrics: list[str] = None,
                 header: bool = True, per_label: bool = True):

        self.dataset = dataset_test
        self.y_true = dataset_test.get_labels_by_bag()
        self.y_pred = classifier.evaluate(dataset_test)
        self.probs = classifier.predict_proba(dataset_test)

        all_metrics = ["precision-score-macro", "precision-score-micro", "average-precision-score-macro",
                       "average-precision-score-micro", "recall-score-macro", "recall-score-micro", "f1-score-macro",
                       "f1-score-micro", "fbeta-score-macro", "fbeta-score-micro", "accuracy-score", "hamming-loss",
                       "jaccard-score-macro", "jaccard-score-micro", "log-loss"]
        if per_label:
            per_label_metrics = ["precision-score", "recall-score", "f1-score", "fbeta-score", "jaccard-score"]
            for metric in per_label_metrics:
                for label in dataset_test.get_labels_name():
                    all_metrics.append(metric+"-"+label)

        if metrics is None:
            metrics = all_metrics
        else:
            for metric in metrics:
                if metric not in all_metrics:
                    raise Exception("Metric ", metric, "is not valid\n", "Metrics availables: ", all_metrics)
        self.header = header
        self.metrics_name = metrics
        self.per_label = per_label
        self.metrics_value = dict()

    def calculate_metrics(self):
        self.metrics_value["precision-score-macro"] = precision_score(self.y_true, self.y_pred, average="macro",
                                                                      zero_division=0)
        self.metrics_value["precision-score-micro"] = precision_score(self.y_true, self.y_pred, average="micro",
                                                                      zero_division=0)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            # When average_precision_score called raise this warming:
            # UserWarning: No positive class found in y_true, recall is set to one for all thresholds.
            self.metrics_value["average-precision-score-macro"] = average_precision_score(self.y_true, self.probs,
                                                                                          average="macro")
            self.metrics_value["average-precision-score-micro"] = average_precision_score(self.y_true, self.probs,
                                                                                          average="micro")
        self.metrics_value["recall-score-macro"] = recall_score(self.y_true, self.y_pred, average="macro",
                                                                zero_division=0)
        self.metrics_value["recall-score-micro"] = recall_score(self.y_true, self.y_pred, average="micro",
                                                                zero_division=0)
        self.metrics_value["f1-score-macro"] = f1_score(self.y_true, self.y_pred, average="macro", zero_division=0)
        self.metrics_value["f1-score-micro"] = f1_score(self.y_true, self.y_pred, average="micro", zero_division=0)
        self.metrics_value["fbeta-score-macro"] = fbeta_score(self.y_true, self.y_pred, beta=1, average="macro",
                                                              zero_division=0)
        self.metrics_value["fbeta-score-micro"] = fbeta_score(self.y_true, self.y_pred, beta=1, average="micro",
                                                              zero_division=0)
        # TODO: ValueError: Only one class present in y_true. ROC AUC score is not defined in that case.
        # self.metrics_value["roc-auc-score-macro"] = roc_auc_score(self.y_true, self.probs, average="macro")
        # self.metrics_value["roc-auc-score-micro"] = roc_auc_score(self.y_true, self.probs, average="micro")
        self.metrics_value["accuracy-score"] = accuracy_score(self.y_true, self.y_pred)
        self.metrics_value["hamming-loss"] = hamming_loss(self.y_true, self.y_pred)
        self.metrics_value["jaccard-score-macro"] = jaccard_score(self.y_true, self.y_pred, average="macro",
                                                                  zero_division=0)
        self.metrics_value["jaccard-score-micro"] = jaccard_score(self.y_true, self.y_pred, average="micro",
                                                                  zero_division=0)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            # When log_loss called raise this warning, it is not true for multilabel classification
            # UserWarning: The y_pred values do not sum to one. Starting from 1.5 thiswill result in an error.
            self.metrics_value["log-loss"] = log_loss(self.y_true, self.probs)

        if self.per_label:
            precision_score_per_label = list(precision_score(self.y_true, self.y_pred, average=None, zero_division=0))
            recall_score_per_label = list(recall_score(self.y_true, self.y_pred, average=None, zero_division=0))
            f1_score_per_label = list(f1_score(self.y_true, self.y_pred, average=None, zero_division=0))
            fbeta_score_per_label = list(fbeta_score(self.y_true, self.y_pred, beta=1, average=None, zero_division=0))
            #roc_auc_score_per_label = list(roc_auc_score(self.y_true, self.probs, average="None"))
            jaccard_score_per_label = list(jaccard_score(self.y_true, self.y_pred, average=None, zero_division=0))
            for i, label in enumerate(self.dataset.get_labels_name()):
                self.metrics_value["precision-score-"+label] = precision_score_per_label[i]
                self.metrics_value["recall-score-"+label] = recall_score_per_label[i]
                self.metrics_value["f1-score-"+label] = f1_score_per_label[i]
                self.metrics_value["fbeta-score-"+label] = fbeta_score_per_label[i]
                # self.metrics_value["roc-auc-score-"+label] = roc_auc_score_per_label[i]
                self.metrics_value["jaccard-score-"+label] = jaccard_score_per_label[i]

    def to_csv(self, path=None):
        self.calculate_metrics()
        header = ""
        if self.header:
            header = ",".join(str(metric) for metric in self.metrics_name)
        values = ",".join(str(self.metrics_value[metric]) for metric in self.metrics_name)
        if path is None:
            print(header)
            print(values)
        else:
            with open(path, mode="a") as f:
                f.write(header)
                f.write(values)

    def to_string(self):
        self.calculate_metrics()
        for metric in self.metrics_name:
            print(metric, ": ", self.metrics_value[metric])
