# -*- coding: utf-8 -*-
"""layer8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZwVw4Z5fOkeBa26BxKK0USl84FMxQl4Y

Layer 8 classification for each labels
"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import svm
from sklearn.preprocessing import StandardScaler

"""load csv

"""

# Load our dataset
train = pd.read_csv('/content/drive/MyDrive/ML/layer8/train.csv')
test = pd.read_csv('/content/drive/MyDrive/ML/layer8/test.csv')
valid = pd.read_csv('/content/drive/MyDrive/ML/layer8/valid.csv')

"""Clean the data to be more handy in up coming work"""

labels = ['label_1','label_2','label_3','label_4']
features = [f"feature_{i}" for i in range(1,769)]
train_feature = train.drop(labels, axis=1)
train_label1 = train['label_1']
train_label2 = train['label_2']
train_label3 = train['label_3']
train_label4 = train['label_4']
valid_feature = valid.drop(labels, axis=1)
valid_label1 = valid['label_1']
valid_label2 = valid['label_2']
valid_label3 = valid['label_3']
valid_label4 = valid['label_4']

"""Run Classifier on the above scaled data Frame"""

classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature,train_label1)
pred_label1 = classifier.predict(valid_feature)

# Evaluate the model
accuracy = accuracy_score(valid_label1, pred_label1)
print("Accuracy of label 1 before feature engineering:", accuracy)

"""Label1

Correlation coefficient for label 1
"""

import numpy as np
corr_matrix1 = train_feature.corr()

# Get upper traingular matrix
upper_1 = corr_matrix1.where(np.triu(np.ones(corr_matrix1.shape), k=1).astype(bool))
features_to_drop_1 = [column for column in upper_1.columns if any(upper_1[column] > 0.44)]

print("No of features to be dropped = ", len(features_to_drop_1))

features_remain = [element for element in train_feature if element not in features_to_drop_1]
print("No of features remaining = ",len(features_remain))

classifier = svm.SVC(kernel="linear")
classifier.fit(train[features_remain], train_label1)
valid_predictions = classifier.predict(valid[features_remain])
accuracy = accuracy_score(valid_label1, valid_predictions)
print("Accuracy after use of correlation co-efficient on L1 :", accuracy)

"""Use ANOVA Selector for label 1"""

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report

new_train_feature_1 = train_feature.drop(features_to_drop_1, axis=1)
new_valid_feature_1 = valid_feature.drop(features_to_drop_1, axis=1)
k = 300

anova_selector = SelectKBest(score_func=f_classif, k=k)

#use anova selector for top k features
train_feature_selected = anova_selector.fit_transform(new_train_feature_1, train_label1)

# Transform the validation features to select the same 'k' features
valid_feature_selected = anova_selector.transform(new_valid_feature_1)

#use svc
classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_selected, train_label1)
valid_predictions = classifier.predict(valid_feature_selected)
accuracy = accuracy_score(valid_label1, valid_predictions)
print("Accuracy after using anova selector :", accuracy)

"""Remaing features after using ANOVA selector for label 1"""

selected_feature_indices = anova_selector.get_support(indices=True)

# Create a DataFrame with the selected features for validation
train_feature_selected_df_1 = pd.DataFrame(train_feature_selected, columns=[features[i] for i in selected_feature_indices])
valid_feature_selected_df_1 = pd.DataFrame(valid_feature_selected, columns=[features[i] for i in selected_feature_indices])
train_feature_selected_df_1.head()
print("Number of rows in the validation features:", valid_feature_selected_df_1.shape[1])

"""Use principal component analysis"""

from sklearn.decomposition import PCA
no_of_components = 150
pca = PCA(n_components=no_of_components)


train_feature_pca_1 = pca.fit_transform(train_feature_selected_df_1)
valid_feature_pca_1 = pca.transform(valid_feature_selected_df_1)


classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_pca_1, train_label1)
valid_predictions = classifier.predict(valid_feature_pca_1)
accuracy = accuracy_score(valid_label1, valid_predictions)
print("Accuracy after PCA :", accuracy)

"""Scaling for label 1"""

sc=StandardScaler()
scaled_train = sc.fit_transform(train_feature_pca_1)
scaled_test = sc.transform(valid_feature_pca_1)

classifier = svm.SVC(kernel="linear")
classifier.fit(scaled_train, train_label1)
valid_predictions = classifier.predict(scaled_test)
accuracy = accuracy_score(valid_label1, valid_predictions)
print("Accuracy after scaling :", accuracy)

ids = test["ID"]
original_test_feature = test.drop("ID", axis=1)
original_test_feature = original_test_feature.drop(features_to_drop_1, axis=1)
original_test_feature_selected = anova_selector.transform(original_test_feature)
original_test_feature_pca = pca.transform(original_test_feature_selected)
# scaled_original_test = sc.transform(original_test_feature_pca)


test_pred_label1 = classifier.predict(original_test_feature_pca)
result_1_df = pd.read_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv')
result_1_df['ID'] = ids
result_1_df['label_1'] = test_pred_label1

result_1_df.to_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv', index=False)
# result_1_df['Predicted labels after feature engineering'] = test_pred_label1
# result_1_df['No of new features'] = no_of_components
# new_column_names = [f'new_feature_{i+1}' for i in range(scaled_original_test.shape[1])]
# pca_df = pd.DataFrame(data=scaled_original_test,columns=new_column_names)
# result_1_df = pd.concat([result_1_df, pca_df], axis=1)
# result_1_df.head()
# result_1_df.to_csv('190569J_label_1.csv',index=False)

"""Label 2"""

classifier = svm.SVC(kernel="linear")

df_train_cleaned_2 = train.dropna()
df_valid_cleaned_2 = valid.dropna()
train_feature_2 = df_train_cleaned_2.drop(labels, axis=1)
train_label2 = df_train_cleaned_2['label_2']
valid_feature_2 = df_valid_cleaned_2.drop(labels, axis=1)
valid_label2 = df_valid_cleaned_2['label_2']

classifier.fit(train_feature_2,train_label2)
pred_label2 = classifier.predict(valid_feature_2)

# Evaluate the model
accuracy = accuracy_score(valid_label2, pred_label2)
print("Accuracy of label 1 before feature engineering:", accuracy)

"""Correlation coefficient for label 2

"""

import numpy as np
corr_matrix2 = train_feature_2.corr()

# Get upper traingular matrix
upper_2 = corr_matrix2.where(np.triu(np.ones(corr_matrix2.shape), k=1).astype(bool))
features_to_drop_2 = [column for column in upper_2.columns if any(upper_2[column] > 0.5)]

print("No of features to be dropped = ", len(features_to_drop_2))

features_remain_2 = [element for element in train_feature_2 if element not in features_to_drop_2]
print("No of features remaining = ",len(features_remain_2))

classifier = svm.SVC(kernel="linear")
classifier.fit(df_train_cleaned_2[features_remain_2], train_label2)
valid_predictions = classifier.predict(df_valid_cleaned_2[features_remain_2])
accuracy = accuracy_score(valid_label2, valid_predictions)
print("Accuracy after use of correlation co-efficient on L2 :", accuracy)

"""Anova selector for label 2"""

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report

new_train_feature_2 = train_feature_2.drop(features_to_drop_2, axis=1)
new_valid_feature_2 = valid_feature_2.drop(features_to_drop_2, axis=1)
k = 400

anova_selector = SelectKBest(score_func=f_classif, k=k)

#use anova selector for top k features
train_feature_selected_2 = anova_selector.fit_transform(new_train_feature_2, train_label2)

# Transform the validation features to select the same 'k' features
valid_feature_selected_2 = anova_selector.transform(new_valid_feature_2)

#use svc
classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_selected_2, train_label2)
valid_predictions = classifier.predict(valid_feature_selected_2)
accuracy = accuracy_score(valid_label2, valid_predictions)
print("Accuracy after using anova selector :", accuracy)

selected_feature_indices = anova_selector.get_support(indices=True)

# Create a DataFrame with the selected features for validation
train_feature_selected_df_2 = pd.DataFrame(train_feature_selected_2, columns=[features[i] for i in selected_feature_indices])
valid_feature_selected_df_2 = pd.DataFrame(valid_feature_selected_2, columns=[features[i] for i in selected_feature_indices])
train_feature_selected_df_2.head()
print("Number of rows in the DataFrame:", valid_feature_selected_df_2.shape[1])

"""PCA on label2"""

from sklearn.decomposition import PCA
no_of_components = 300
pca = PCA(n_components=no_of_components)


train_feature_pca_2 = pca.fit_transform(train_feature_selected_df_2)
valid_feature_pca_2 = pca.transform(valid_feature_selected_df_2)


classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_pca_2, train_label2)
valid_predictions = classifier.predict(valid_feature_pca_2)
accuracy = accuracy_score(valid_label2, valid_predictions)
print("Accuracy after PCA :", accuracy)

"""Scaling"""

sc=StandardScaler()
scaled_train = sc.fit_transform(train_feature_pca_2)
scaled_valid = sc.transform(valid_feature_pca_2)

classifier = svm.SVC(kernel="linear")
classifier.fit(scaled_train, train_label2)
valid_predictions = classifier.predict(scaled_valid)
accuracy = accuracy_score(valid_label2, valid_predictions)
print("Accuracy after scaling :", accuracy)

original_test_feature = test.drop("ID", axis=1)
original_test_feature = original_test_feature.drop(features_to_drop_2, axis=1)

original_test_feature_selected = anova_selector.transform(original_test_feature)
original_test_feature_pca = pca.transform(original_test_feature_selected)
# scaled_original_test = sc.transform(original_test_feature_pca)

test_pred_label2 = classifier.predict(original_test_feature_pca)
result_2_df = pd.read_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv')
result_2_df['label_2'] = test_pred_label2
result_2_df.to_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv', index=False)
# result_1_df['Predicted labels after feature engineering'] = test_pred_label1
# result_1_df['No of new features'] = no_of_components
# new_column_names = [f'new_feature_{i+1}' for i in range(scaled_original_test.shape[1])]
# pca_df = pd.DataFrame(data=scaled_original_test,columns=new_column_names)
# result_1_df = pd.concat([result_1_df, pca_df], axis=1)
# result_1_df.head()
# result_1_df.to_csv('190569J_label_1.csv',index=False)

"""Label 3

"""

classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature,train_label3)
pred_label3 = classifier.predict(valid_feature)

# Evaluate the model
accuracy = accuracy_score(valid_label3, pred_label3)
print("Accuracy of label 1 before feature engineering:", accuracy)

"""use correlation coedfficient label3"""

import numpy as np
corr_matrix3 = train_feature.corr()

# Get upper traingular matrix
upper_3 = corr_matrix3.where(np.triu(np.ones(corr_matrix3.shape), k=1).astype(bool))
features_to_drop_3 = [column for column in upper_3.columns if any(upper_3[column] > 0.4)]

print("No of features to be dropped = ", len(features_to_drop_3))

features_remain_3 = [element for element in train_feature if element not in features_to_drop_3]
print("No of features remaining = ",len(features_remain_3))

classifier = svm.SVC(kernel="linear")
classifier.fit(train[features_remain_3], train_label3)
valid_predictions = classifier.predict(valid[features_remain_3])
accuracy = accuracy_score(valid_label3, valid_predictions)
print("Accuracy after use of correlation co-efficient on L3 :", accuracy)

"""Anova Selector"""

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report

new_train_feature_3 = train_feature.drop(features_to_drop_3, axis=1)
new_valid_feature_3 = valid_feature.drop(features_to_drop_3, axis=1)
k = 100

anova_selector = SelectKBest(score_func=f_classif, k=k)

#use anova selector for top k features
train_feature_selected_3 = anova_selector.fit_transform(new_train_feature_3, train_label3)

# Transform the validation features to select the same 'k' features
valid_feature_selected_3 = anova_selector.transform(new_valid_feature_3)

#use svc
classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_selected_3, train_label3)
valid_predictions = classifier.predict(valid_feature_selected_3)
accuracy = accuracy_score(valid_label3, valid_predictions)
print("Accuracy after using anova selector :", accuracy)

selected_feature_indices = anova_selector.get_support(indices=True)

# Create a DataFrame with the selected features for validation
train_feature_selected_df_3 = pd.DataFrame(train_feature_selected_3, columns=[features[i] for i in selected_feature_indices])
valid_feature_selected_df_3 = pd.DataFrame(valid_feature_selected_3, columns=[features[i] for i in selected_feature_indices])
train_feature_selected_df_3.head()
print("Number of rows in the DataFrame:", valid_feature_selected_df_3.shape[1])

"""PCA on label 3

"""

from sklearn.decomposition import PCA
no_of_components = 70
pca = PCA(n_components=no_of_components)


train_feature_pca_3 = pca.fit_transform(train_feature_selected_df_3)
valid_feature_pca_3 = pca.transform(valid_feature_selected_df_3)


classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_pca_3, train_label3)
valid_predictions = classifier.predict(valid_feature_pca_3)
accuracy = accuracy_score(valid_label3, valid_predictions)
print("Accuracy after PCA :", accuracy)

"""Scaling label3"""

sc=StandardScaler()
scaled_train = sc.fit_transform(train_feature_pca_3)
scaled_test = sc.transform(valid_feature_pca_3)

classifier = svm.SVC(kernel="linear")
classifier.fit(scaled_train, train_label3)
valid_predictions = classifier.predict(scaled_test)
accuracy = accuracy_score(valid_label3, valid_predictions)
print("Accuracy after scaling :", accuracy)

original_test_feature = test.drop("ID", axis=1)
original_test_feature = original_test_feature.drop(features_to_drop_3, axis=1)

original_test_feature_selected = anova_selector.transform(original_test_feature)
original_test_feature_pca = pca.transform(original_test_feature_selected)
scaled_original_test = sc.transform(original_test_feature_pca)

test_pred_label3 = classifier.predict(scaled_original_test)
result_3_df = pd.read_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv')
result_3_df['label_3'] = test_pred_label3
result_3_df.to_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv', index=False)
# result_1_df['Predicted labels after feature engineering'] = test_pred_label1
# result_1_df['No of new features'] = no_of_components
# new_column_names = [f'new_feature_{i+1}' for i in range(scaled_original_test.shape[1])]
# pca_df = pd.DataFrame(data=scaled_original_test,columns=new_column_names)
# result_1_df = pd.concat([result_1_df, pca_df], axis=1)
# result_1_df.head()
# result_1_df.to_csv('190569J_label_1.csv',index=False)

"""Label 4"""

classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature,train_label4)
pred_label4 = classifier.predict(valid_feature)

# Evaluate the model
accuracy = accuracy_score(valid_label4, pred_label4)
print("Accuracy of label 1 before feature engineering:", accuracy)

"""use correleation coefficiecnt label 4"""

import numpy as np
corr_matrix4 = train_feature.corr()

# Get upper traingular matrix
upper_4 = corr_matrix4.where(np.triu(np.ones(corr_matrix4.shape), k=1).astype(bool))
features_to_drop_4 = [column for column in upper_4.columns if any(upper_4[column] > 0.5)]

print("No of features to be dropped = ", len(features_to_drop_4))

features_remain_4 = [element for element in train_feature if element not in features_to_drop_4]
print("No of features remaining = ",len(features_remain_4))

classifier = svm.SVC(kernel="linear")
classifier.fit(train[features_remain_4], train_label4)
valid_predictions = classifier.predict(valid[features_remain_4])
accuracy = accuracy_score(valid_label4, valid_predictions)
print("Accuracy after use of correlation co-efficient on L4 :", accuracy)

"""Use ANOVA selector"""

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report

new_train_feature_4 = train_feature.drop(features_to_drop_4, axis=1)
new_valid_feature_4 = valid_feature.drop(features_to_drop_4, axis=1)
k = 400

anova_selector = SelectKBest(score_func=f_classif, k=k)

#use anova selector for top k features
train_feature_selected_4 = anova_selector.fit_transform(new_train_feature_4, train_label4)

# Transform the validation features to select the same 'k' features
valid_feature_selected_4 = anova_selector.transform(new_valid_feature_4)

#use svc
classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_selected_4, train_label4)
valid_predictions = classifier.predict(valid_feature_selected_4)
accuracy = accuracy_score(valid_label4, valid_predictions)
print("Accuracy after using anova selector :", accuracy)

selected_feature_indices = anova_selector.get_support(indices=True)

# Create a DataFrame with the selected features for validation
train_feature_selected_df_4 = pd.DataFrame(train_feature_selected_4, columns=[features[i] for i in selected_feature_indices])
valid_feature_selected_df_4 = pd.DataFrame(valid_feature_selected_4, columns=[features[i] for i in selected_feature_indices])
train_feature_selected_df_4.head()
print("Number of columns in the features:", valid_feature_selected_df_4.shape[1])

"""PCA label4"""

from sklearn.decomposition import PCA
no_of_components = 200
pca = PCA(n_components=no_of_components)


train_feature_pca_4 = pca.fit_transform(train_feature_selected_df_4)
valid_feature_pca_4 = pca.transform(valid_feature_selected_df_4)


classifier = svm.SVC(kernel="linear")
classifier.fit(train_feature_pca_4, train_label4)
valid_predictions = classifier.predict(valid_feature_pca_4)
accuracy = accuracy_score(valid_label4, valid_predictions)
print("Accuracy after PCA :", accuracy)

"""Scaling label4"""

sc=StandardScaler()
scaled_train = sc.fit_transform(train_feature_pca_4)
scaled_valid = sc.transform(valid_feature_pca_4)

classifier = svm.SVC(kernel="linear")
classifier.fit(scaled_train, train_label4)
valid_predictions = classifier.predict(scaled_valid)
accuracy = accuracy_score(valid_label4, valid_predictions)
print("Accuracy after scaling :", accuracy)

original_test_feature = test.drop("ID", axis=1)
original_test_feature = original_test_feature.drop(features_to_drop_4, axis=1)

original_test_feature_selected = anova_selector.transform(original_test_feature)
original_test_feature_pca = pca.transform(original_test_feature_selected)
scaled_original_test = sc.transform(original_test_feature_pca)

test_pred_label4 = classifier.predict(scaled_original_test)
result_4_df = pd.read_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv')
result_4_df['label_4'] = test_pred_label4
result_4_df.to_csv('/content/drive/MyDrive/ML/layer8/test_with_predictions.csv', index=False)
# result_1_df['Predicted labels after feature engineering'] = test_pred_label1
# result_1_df['No of new features'] = no_of_components
# new_column_names = [f'new_feature_{i+1}' for i in range(scaled_original_test.shape[1])]
# pca_df = pd.DataFrame(data=scaled_original_test,columns=new_column_names)
# result_1_df = pd.concat([result_1_df, pca_df], axis=1)
# result_1_df.head()
# result_1_df.to_csv('190569J_label_1.csv',index=False)