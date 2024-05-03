import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold, KFold

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression


class MultiModelClassifier:
    def __init__(self, dataset, k_n_splits=5, k_random_state=None, is_shuffled=False, stratify=False, l_models=None,
                 scaler=None, cible='target'):
        self.df = dataset
        self.n_splits = k_n_splits
        self.random_state = k_random_state
        self.shuffle = is_shuffled
        self.cible = cible
        if not stratify:
            self.kfold = KFold(n_splits=self.n_splits, random_state=self.random_state, shuffle=self.shuffle)
        else:
            self.kfold = StratifiedKFold(n_splits=self.n_splits, random_state=self.random_state, shuffle=self.shuffle)
        self.splits = self.kfold.split(self.df, self.df[self.cible])
        # The column used for stratification is the target, here df['target']
        self.train_sets = []
        self.test_sets = []
        self.models = l_models
        self.cat = self.df.select_dtypes(include=['object']).columns.to_list()
        self.num = self.df.select_dtypes(exclude=['object']).columns.to_list()
        if self.df[cible].dtype == 'object':
            self.cat.remove(self.cible)
        else:
            self.num.remove(self.cible)
        if scaler:
            self.scl = scaler
        else:
            self.scl = StandardScaler()
        self.dummies()
        self.separate_quali_quanti()
        self.result = dict()
        for key in self.models.keys():
            list_score = []
            self.result[key] = dict()
            for i in range(len(self.train_sets)):
                sub = f"subset:{i + 1}"
                self.result[key][sub] = dict()
                self.my_fit(self.models[key]['model'], self.train_sets[i][0], self.train_sets[i][1])
                self.pred = pd.Series(self.my_predict(self.models[key]['model'], self.test_sets[i][0]), name='pred')
                self.act = self.test_sets[i][1].reset_index(drop=True).rename('actual')
                res = self.evaluate(self.pred, self.act)
                list_score.append(res)
                self.result[key][sub]['accuracy'] = res[0]
                self.result[key][sub]['precision'] = res[1]
                self.result[key][sub]['recall'] = res[2]
                self.result[key][sub]['f1'] = res[3]
            array_score = np.array(list_score)
            self.result[key]['overall'] = {
                'accuracy': np.round(array_score.mean(axis=0)[0], 3),
                'precision': np.round(array_score.mean(axis=0)[1], 3),
                'recall': np.round(array_score.mean(axis=0)[2], 3),
                'f1': np.round(array_score.mean(axis=0)[3], 3),
            }

    def check_splits(self):
        for n, (train_index, test_index) in enumerate(self.splits):
            print(
                f'SPLIT NO {n + 1}\nTRAINING SET SIZE: {np.round(len(train_index) / (len(train_index) + len(test_index)), 2)}' +
                f'\tTEST SET SIZE: {np.round(len(test_index) / (len(train_index) + len(test_index)), 2)}\nPROPORTION OF TARGET IN THE TRAINING SET\n' +
                f'{self.df.loc[test_index, self.cible].value_counts() / len(self.df.loc[test_index, self.cible])}\nPROPORTION OF TARGET IN THE TEST SET\n' +
                f'{self.df.loc[train_index, self.cible].value_counts() / len(self.df.loc[train_index, self.cible])}\n\n')

    def separate_quali_quanti(self):
        self.data = self.df.drop(columns=[self.cible])
        for n, (train_index, test_index) in enumerate(self.splits):
            self.scl.fit(self.data.loc[train_index, :])
            self.train_sets.append(
                [pd.DataFrame(self.scl.transform(self.data.loc[train_index, :]), columns=self.data.columns),
                 self.df.loc[train_index, self.cible]])
            self.test_sets.append(
                [pd.DataFrame(self.scl.transform(self.data.loc[test_index, :]), columns=self.data.columns),
                 self.df.loc[test_index, self.cible]])
        # Train sets is a list of list of Dataframe. Each inner list contains (X, y)

    def dummies(self):
        enc = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        one_hot = pd.DataFrame(enc.fit_transform(pd.DataFrame(self.df[self.cat])))
        one_hot.columns = enc.get_feature_names_out(self.df[self.cat].columns)
        self.df = pd.concat([self.df.drop(columns=self.cat), one_hot], axis=1)

    def my_fit(self, model, x, y):
        model.fit(x, y)

    def my_predict(self, model, x):
        return model.predict(x)

    def evaluate(self, act, pred):
        concat = pd.concat([act, pred], axis=1)
        concat['same'] = concat['actual'] == concat['pred']
        TP = concat[(concat['actual'] == 'sick') & (concat['pred'] == 'sick')].shape[0]
        TN = concat[(concat['actual'] == 'safe') & (concat['pred'] == 'safe')].shape[0]
        FP = concat[(concat['actual'] == 'sick') & (concat['pred'] == 'safe')].shape[0]
        FN = concat[(concat['actual'] == 'safe') & (concat['pred'] == 'sick')].shape[0]
        acc = np.round(concat['same'].sum() / len(concat), 2)
        precision = np.round(TP / (TP + FP), 2)
        recall = np.round(TP / (TP + FN), 2)
        f1 = np.round((2 * precision * recall) / (precision + recall), 2)
        return acc, precision, recall, f1

    def display(self):
        for key, value in self.result.items():
            print(key)
            for subset, val in value.items():
                print(f"{subset}: {val}")

