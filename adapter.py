import gensim
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer


class DqatClassifier:
    def __init__(self, classifier, vector_size=100):
        self.classifier = classifier
        self.mlb = MultiLabelBinarizer()
        self.vector_size = vector_size
        self.report = None
        self.model = None
        self.word2vec_model = None

    def fit(self, X, y):
        fit_x = [" ".join(x) for x in X]

        # self.word2vec_model = gensim.models.Word2Vec(sentences=fit_x, vector_size=200, window=3,
        #                                              min_count=2,
        #                                              workers=40)

        X = fit_x
        y = self.mlb.fit_transform(y)

        self.model = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', MultiOutputClassifier(self.classifier()))
        ])
        self.model.fit(X, y)

    def headers_to_vec(self, headers):
        # Get the vector for each word and take the mean of the vectors
        model = self.word2vec_model
        vector_size = self.vector_size

        vectors = [model.wv[word] for word in headers if word in model.wv]
        if len(vectors) > 0:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(vector_size)

    def predict(self, input):
        input = [" ".join(input)]

        result_binary = self.model.predict(input)
        result = self.mlb.inverse_transform(result_binary)
        return result[0] if result else []


class DqatEstimator:

    def __init__(self, metrics, estimator, vector_size):
        self.metrics = metrics
        self.estimator = estimator
        self.vector_size = vector_size
        self.word2vec_model = None
        self.models = None

    def fit(self, X, y):
        fit_x = [" ".join(x) for x in X]

        self.word2vec_model = gensim.models.Word2Vec(sentences=fit_x, vector_size=200, window=3,
                                                     min_count=2,
                                                     workers=40)
        # Convert headers to feature vectors
        X = np.array([self.headers_to_vec(x) for x in fit_x])

        models = {}
        for metric in self.metrics:
            model = self.estimator()
            model.fit(X, y[metric])
            models[metric] = model

        self.models = models

    def headers_to_vec(self, headers):
        # Get the vector for each word and take the mean of the vectors
        model = self.word2vec_model
        vector_size = self.vector_size

        vectors = [model.wv[word] for word in headers if word in model.wv]
        if len(vectors) > 0:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(vector_size)

    def predict(self, input):
        input = [self.headers_to_vec(" ".join(input))]

        prediction = {}
        for metric in self.metrics:
            model = self.models[metric]
            predicted_tags_binary = model.predict(input)
            prediction[metric] = predicted_tags_binary[0] if predicted_tags_binary else 0

        return prediction
