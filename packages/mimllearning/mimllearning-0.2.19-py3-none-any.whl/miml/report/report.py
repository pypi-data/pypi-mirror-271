import pandas as pd
from sklearn.metrics import hamming_loss, accuracy_score, fbeta_score, jaccard_score, log_loss, \
    roc_auc_score, f1_score, precision_score, recall_score, average_precision_score


class Report:

    def __init__(self, metrics=None, header=True, per_label=False):
        self.header = header
        self.metrics_name = metrics
        self.per_label = per_label
        self.metrics_value = dict()

    def calculate_metrics(self, y_true, y_pred):
        self.metrics_value["precision-score-macro"] = precision_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["precision-score-micro"] = precision_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["average-precision-score-macro"] = average_precision_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["average-precision-score-micro"] = average_precision_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["recall-score-macro"] = recall_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["recall-score-micro"] = recall_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["f1-score-macro"] = f1_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["f1-score-micro"] = f1_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["fbeta-score-macro"] = fbeta_score(y_true, y_pred, beta=1, average="macro", zero_division=0)
        self.metrics_value["fbeta-score-micro"] = fbeta_score(y_true, y_pred, beta=1, average="micro", zero_division=0)
        self.metrics_value["roc-auc-score-macro"] = roc_auc_score(y_true, y_pred, average="macro")
        self.metrics_value["roc-auc-score-micro"] = roc_auc_score(y_true, y_pred, average="micro")
        self.metrics_value["accuracy-score"] = accuracy_score(y_true, y_pred)
        self.metrics_value["hamming-loss"] = hamming_loss(y_true, y_pred)
        self.metrics_value["jaccard-score"] = jaccard_score(y_true, y_pred, zero_division=0)
        self.metrics_value["log-loss"] = log_loss(y_true, y_pred)

        if self.per_label:
            self.metrics_value["precision-score-per-label"] = precision_score(y_true, y_pred, average="None")
            self.metrics_value["average-precision-score-per-label"] = precision_score(y_true, y_pred, average="None")
            self.metrics_value["recall-score-per-label"] = recall_score(y_true, y_pred, average="None")
            self.metrics_value["f1-score-per-label"] = f1_score(y_true, y_pred, average="None")
            self.metrics_value["fbeta-score-per-label"] = fbeta_score(y_true, y_pred, beta=1, average="None")
            self.metrics_value["roc-auc-score-per-label"] = roc_auc_score(y_true, y_pred, average="None")

    def to_csv(self, y_true, y_pred):
        self.calculate_metrics(y_true, y_pred)
        if self.header:
            header = ""

    def to_string(self, y_true, y_pred):
        self.calculate_metrics(y_true, y_pred)
        if self.metrics_name is None:
            for metric in self.metrics_value.items():
                print(metric[0], ": ", metric[1])

    def save_report(self, path):

        try:
            csv = pd.read_csv(path)
        except FileNotFoundError:
            csv = pd.DataFrame()
        results = pd.DataFrame(self.metrics_value)
        df = pd.concat([csv, results])
        df.to_csv(path, mode='a', index=False, header=self.header)
