import gensim
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

headers = []
tags = []


class DqatClassifier:
    def __init__(self, classifier):
        self.classifier = classifier
        self.mlb = MultiLabelBinarizer()
        self.report = None
        self.model = None
        self.word2vec_model = None

    def fit(self, X, Y):
        X = [" ".join(x) for x in X]
        y = self.mlb.fit_transform(Y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        self.model = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', OneVsRestClassifier(self.classifier))
        ])
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        self.report = \
            classification_report(y_test, y_pred, target_names=self.mlb.classes_, output_dict=True, zero_division=0)[
                'samples avg']

        self.report['accuracy'] = accuracy_score(y_test, y_pred)

    def predict(self, input):
        input = [" ".join(input)]
        result_binary = self.model.predict(input)
        result = self.mlb.inverse_transform(result_binary)
        return result[0] if result else []


decision_tree = DqatClassifier(DecisionTreeClassifier(random_state=142))
decision_tree.fit(headers, tags)
print(f'Decision tree {decision_tree.report}', )

svc_linear = DqatClassifier(SVC(kernel='linear', ))
svc_linear.fit(headers, tags)
print(f'SVC Linead {svc_linear.report}', )

random_forest = DqatClassifier(RandomForestClassifier())
random_forest.fit(headers, tags)
print(f'Random Forest {random_forest.report}', )

logistic_regression = DqatClassifier(LogisticRegression(random_state=142))
logistic_regression.fit(headers, tags)
print(f'Logistic Regression {logistic_regression.report}', )
