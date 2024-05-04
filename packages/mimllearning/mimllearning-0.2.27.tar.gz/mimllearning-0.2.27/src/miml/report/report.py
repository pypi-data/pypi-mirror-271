from sklearn.metrics import hamming_loss, accuracy_score, fbeta_score, jaccard_score, log_loss, \
    roc_auc_score, f1_score, precision_score, recall_score, average_precision_score


class Report:

    def __init__(self, metrics=None, header=True, per_label=True):
        self.header = header
        all_metrics = ["precision-score-macro", "precision-score-micro", "average-precision-score-macro",
                       "average-precision-score-micro", "recall-score-macro", "recall-score-micro", "f1-score-macro",
                       "f1-score-micro", "fbeta-score-macro", "fbeta-score-micro", "accuracy-score", "hamming-loss",
                       "jaccard-score-macro", "jaccard-score-micro", "log-loss"]
        if per_label:
            all_metrics += ["precision-score-per-label", "average-precision-score-per-label", "recall-score-per-label",
                            "f1-score-per-label", "fbeta-score-per-label", "jaccard-score-per-label"]

        if metrics is None:
            metrics = all_metrics
        else:
            for metric in metrics:
                if metric not in all_metrics:
                    raise Exception("Metric ", metric, "is not valid\n", "Metrics availables: ", all_metrics)
        self.metrics_name = metrics
        self.per_label = per_label
        self.metrics_value = dict()

    def calculate_metrics(self, y_true, y_pred):
        self.metrics_value["precision-score-macro"] = precision_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["precision-score-micro"] = precision_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["average-precision-score-macro"] = average_precision_score(y_true, y_pred, average="macro")
        self.metrics_value["average-precision-score-micro"] = average_precision_score(y_true, y_pred, average="micro")
        self.metrics_value["recall-score-macro"] = recall_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["recall-score-micro"] = recall_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["f1-score-macro"] = f1_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["f1-score-micro"] = f1_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["fbeta-score-macro"] = fbeta_score(y_true, y_pred, beta=1, average="macro", zero_division=0)
        self.metrics_value["fbeta-score-micro"] = fbeta_score(y_true, y_pred, beta=1, average="micro", zero_division=0)
        # self.metrics_value["roc-auc-score-macro"] = roc_auc_score(y_true, y_pred, average="macro")
        # self.metrics_value["roc-auc-score-micro"] = roc_auc_score(y_true, y_pred, average="micro")
        self.metrics_value["accuracy-score"] = accuracy_score(y_true, y_pred)
        self.metrics_value["hamming-loss"] = hamming_loss(y_true, y_pred)
        self.metrics_value["jaccard-score-macro"] = jaccard_score(y_true, y_pred, average="macro", zero_division=0)
        self.metrics_value["jaccard-score-micro"] = jaccard_score(y_true, y_pred, average="micro", zero_division=0)
        self.metrics_value["log-loss"] = log_loss(y_true, y_pred)

        if self.per_label:
            self.metrics_value["precision-score-per-label"] = precision_score(y_true, y_pred, average=None,
                                                                              zero_division=0).flatten()
            self.metrics_value["average-precision-score-per-label"] = precision_score(y_true, y_pred, average=None,
                                                                                      zero_division=0).flatten()
            self.metrics_value["recall-score-per-label"] = recall_score(y_true, y_pred, average=None,
                                                                        zero_division=0).flatten()
            self.metrics_value["f1-score-per-label"] = f1_score(y_true, y_pred, average=None, zero_division=0).flatten()
            self.metrics_value["fbeta-score-per-label"] = fbeta_score(y_true, y_pred, beta=1, average=None,
                                                                      zero_division=0).flatten()
            # self.metrics_value["roc-auc-score-per-label"] = roc_auc_score(y_true, y_pred, average="None")
            self.metrics_value["jaccard-score-per-label"] = jaccard_score(y_true, y_pred, average=None,
                                                                          zero_division=0).flatten()

    def to_csv(self, y_true, y_pred, path=None):
        self.calculate_metrics(y_true, y_pred)
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

    def to_string(self, y_true, y_pred):
        self.calculate_metrics(y_true, y_pred)
        for metric in self.metrics_name:
            print(metric, ": ", self.metrics_value[metric])

