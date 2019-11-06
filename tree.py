# -*- coding: utf-8 -*-

import numpy as np

class Tree(object):
    def __init__(self,  max_depth=6 , min_samples = 1):
        self.feature = None
        self.label = None
        self.n_samples = None
        self.gain = None
        self.left = None
        self.right = None
        self.threshold = None
        self.max_depth = max_depth
        self.depth = 0
        self.min_samples = min_samples

    def build(self, features, target, criterion='gini'):
        self.n_samples = features.shape[0]
        #print(self.n_samples)

        #окончание рекурсии
        if len(np.unique(target)) == 1:
            self.label = target[0]
            return

        best_gain = 0.0
        best_feature = None
        best_threshold = None



        if criterion in {'gini', 'entropy'}:
            self.label = max(target, key=lambda c: len(target[target == c]))
        else:
            self.label = np.mean(target)



        impurity_node = self._calc_impurity(criterion, target)

        for col in range(features.shape[1]):
            feature_level = np.unique(features[:, col])
            thresholds = (feature_level[:-1] + feature_level[1:]) / 2.0

            # Поиск порогов высоким приростом информации
            for threshold in thresholds:
                target_l = target[features[:, col] <= threshold]
                impurity_l = self._calc_impurity(criterion, target_l)
                n_l = target_l.shape[0] / self.n_samples

                target_r = target[features[:, col] > threshold]
                impurity_r = self._calc_impurity(criterion, target_r)
                n_r = target_r.shape[0] / self.n_samples


                # Получение информации: IG = узел- (левый + правый)
                ig = impurity_node - (n_l * impurity_l + n_r * impurity_r)

                if ig > best_gain or best_threshold is None or best_feature is None:
                    best_gain = ig
                    best_feature = col
                    best_threshold = threshold

        self.feature = best_feature
        self.gain = best_gain
        self.threshold = best_threshold
        if  self.depth < self.max_depth:
            self._divide_tree(features, target, criterion)
        else:
            self.feature = None

    def _divide_tree(self, features, target, criterion):
        features_l = features[features[:, self.feature] <= self.threshold]
        target_l = target[features[:, self.feature] <= self.threshold]
        self.left = Tree(self.max_depth)
        self.left.depth = self.depth + 1
        self.left.build(features_l, target_l, criterion)

        features_r = features[features[:, self.feature] > self.threshold]
        target_r = target[features[:, self.feature] > self.threshold]
        self.right = Tree(self.max_depth)
        self.right.depth = self.depth + 1
        self.right.build(features_r, target_r, criterion)

    def _calc_impurity(self, criterion, target):
        classes = np.unique(target)

        if criterion == 'gini':
            return self._gini(target, classes)
        elif criterion == 'entropy':
            return self._entropy(target, classes)
        elif criterion == 'mae':
            return self._mae(target)
        elif criterion == 'mse':
            return self._mse(target)
        else:
            return self._gini(target, classes)

    def _gini(self, target, classes):
        n = target.shape[0]
        return 1.0 - sum([(len(target[target == c]) / n) ** 2 for c in classes])

    def _entropy(self, target, classes):
        n = target.shape[0]
        entropy = 0.0
        for c in classes:
            p = len(target[target == c]) / n
            if p > 0.0:
                entropy -= p * np.log2(p)
        return entropy

    def _mae(self, target):
        y_hat = np.mean(target)
        return 1.0 - np.abs(target - y_hat).mean()

    def _mse(self, target):
        y_hat = np.mean(target)
        return np.square(target - y_hat).mean()

    #Обрезка дерева решений.
    def prune(self,  max_depth,  n_samples):
        if self.feature is None:
            return

        self.left.prune(max_depth, n_samples)
        self.right.prune(max_depth,  n_samples)

        pruning = False
    #    print(n_samples < self.min_samples  )
    #    print(self.min_samples)
    #    print(n_samples)
    #    print(self.depth >= max_depth)

        #условие обрезки.
        if (self.depth >= max_depth) or (self.min_samples > n_samples):
            pruning = True


        if pruning is True:
            self.left = None
            self.right = None
            self.feature = None

    def predict(self, d):
        if self.feature is None:
            return self.label
        else:
            if d[self.feature] <= self.threshold:
                return self.left.predict(d)
            else:
                return self.right.predict(d)



class DecisionTreeRegressor(object):
    def __init__(self, criterion='mse', max_depth=3, min_samples = 1):
        self.root = None
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples = min_samples

    def fit(self, features, target):
        self.root = Tree(self.max_depth, self.min_samples)
        self.root.build(features, target, self.criterion)
        self.root.prune(
            self.max_depth,
            self.root.n_samples
        )

    def predict(self, features):
        return np.array([self.root.predict(f) for f in features])


class DecisionTreeClassifier(object):
    def __init__(self, criterion='gini', max_depth=3, min_samples = 1):
        self.root = None
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples = min_samples

    def fit(self, features, target):
        self.root = Tree(self.max_depth, self.min_samples)
        self.root.build(features, target, self.criterion)
        self.root.prune(
            self.max_depth,
            self.root.n_samples
        )


    def predict(self, features):
        return np.array([self.root.predict(f) for f in features])
