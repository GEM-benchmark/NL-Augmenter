import numpy as np
from scipy import sparse as sp


class OneHotEncoder():
    """
    Transforms categorical features to continuous numeric features.
    """
    def fit(self, X):
        data = np.asarray(X)
        unique_feats = []
        offset = 0
        for i in range(data.shape[1]):
            feat_set_i = set(data[:, i])
            d = {val: i + offset for i, val in enumerate(feat_set_i)}
            unique_feats.append(d)
            offset += len(feat_set_i)

        self.unique_feats = unique_feats
        return self

    def transform(self, X, sparse=True):
        X = np.atleast_2d(X)
        if sparse:
            one_hot_matrix = sp.lil_matrix(
                (len(X), sum(len(i) for i in self.unique_feats)))
        else:
            one_hot_matrix = np.zeros(
                (len(X), sum(len(i) for i in self.unique_feats)), bool)
        for i, vec in enumerate(X):
            for j, val in enumerate(vec):
                if val in self.unique_feats[j]:
                    one_hot_matrix[i, self.unique_feats[j][val]] = 1.0

        return sp.csr_matrix(one_hot_matrix) if sparse else one_hot_matrix
