import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
# 為了處理方便，把 'train.csv' 和 'test.csv' 合併起來，'test.csv'的 Weather 欄位用 0 補起來。
df = pd.read_csv('data/train.csv')
df_test = pd.read_csv('data/test.csv')
df_test['Label'] = np.zeros((len(df_test),))

# 以 train_end_idx 作為 'train.csv' 和 'test.csv' 分界列，
train_end_idx = len(df)
df = pd.concat([df, df_test], sort=False)

# 將非數值欄位拿掉
# df = df.drop(columns = [col for col in df.columns if df[col].dtype == np.object])

# or encode object feature
object_columns = [col for col in df.columns if df[col].dtype == np.object]
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
for object_col in object_columns:
    df[object_col] = labelencoder.fit_transform(df[object_col])

# Fill missing value
# 將 missing value 補 median
# for col in df.columns:
#     median = df[col].median()
#     df[col] = df[col].fillna(median)
# df_imputed = df.reset_index(drop=True).drop(columns=['Label'])

# or use KNN imputer to fill missing value
# from sklearn.impute import KNNImputer
# imputer = KNNImputer(n_neighbors=2)
# df_imputed = pd.DataFrame(imputer.fit_transform(df.drop(columns=['Label'])))

# # or use Missing forest
import sys
import sklearn.neighbors._base
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest
imputer = MissForest(max_iter=10)
df_imputed = pd.DataFrame(imputer.fit_transform(df.drop(columns = ['Label'])))

# normalization
# keep label
columns_label = df['Label'].reset_index(drop=True)

# normalization
df_norm=(df_imputed-df_imputed.min())/(df_imputed.max()-df_imputed.min())

# add label back
df_preprocess = pd.concat([df_norm, columns_label], axis=1)
# df_preprocess = df_preprocess.rename(columns={21: "Label"})

# split 
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(
    df_preprocess.drop(columns = ['Label']).values[:train_end_idx, :], 
    df_preprocess['Label'].values[:train_end_idx], test_size=0.2)

X_test = df_preprocess.drop(columns = ['Label']).values[train_end_idx:, :]

# deal with imbalance
from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=42)
X_train, y_train = sm.fit_resample(X_train, y_train)

# train
# AdaBooast classifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, f1_score

Ada_clf = AdaBoostClassifier(n_estimators=100, random_state=0)
Ada_clf.fit(X_train, y_train)

y_pred_Ada = Ada_clf.predict(X_val)
print("Adaboost-encode_MF_normalization")
print('Accuracy: %f' % accuracy_score(y_val, y_pred_Ada))
print('f1-score: %f' % f1_score(y_val, y_pred_Ada))

ans_pred = Ada_clf.predict(X_test)
df_sap = pd.DataFrame(ans_pred.astype(int), columns = ['Label'])
df_sap.to_csv('result/AdaBoost/encode_MF_normalization.csv',  index_label = 'Id')