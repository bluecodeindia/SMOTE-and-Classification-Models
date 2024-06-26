# -*- coding: utf-8 -*-


from google.colab import drive
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import KMeansSMOTE
from imblearn.over_sampling import SVMSMOTE
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import ADASYN
import numpy as np
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Mount Google Drive
drive.mount('/content/drive')

# Path to the data file on Google Drive
data_path = 'Data With Label.csv'

# Load data into a Pandas DataFrame
data = pd.read_csv(data_path)

# Print the loaded data
print(data.head())

data1 = data.values

X = data1[:,:-1]
y = data1[:,-1]

X = np.nan_to_num(X, nan=0)
y = np.nan_to_num(y, nan=0)

import numpy as np

def create_sliding_window_packets(X, y, seq_length):
    X_packets = []
    y_packets = []

    num_packets = len(X) - seq_length -1

    for i in range(num_packets):
        X_packet = X[i:i+seq_length]
        y_packet = y[i+seq_length]

        X_packets.append(X_packet)
        y_packets.append(y_packet)

    return np.array(X_packets), np.array(y_packets)

# Define the sequence length
seq_length = 5

# Create packets based on the sliding window with sequence length
X_packets, y_packets = create_sliding_window_packets(X, y, seq_length)

X_packets = X_packets.reshape((-1,seq_length*11))

X = X_packets
y = y_packets

X.shape

# Instantiate the SMOTE oversampling technique
smote = SMOTE(random_state=42)

# Apply SMOTE to the dataset
X_resampled_smote, y_resampled_smote = smote.fit_resample(X, y)

# Print the resampled dataset shape
print("Original dataset shape:", X.shape, y.shape)
print("Resampled dataset shape:", X_resampled_smote.shape, y_resampled_smote.shape)

# Instantiate the KMeansSMOTE oversampler
kmeans_smote = KMeansSMOTE(cluster_balance_threshold=0.001, random_state=42)

# Apply KMeansSMOTE to the dataset
X_resampled_kmean, y_resampled_kmean = kmeans_smote.fit_resample(X, y)

# Print the resampled data
print("Original dataset shape:", X.shape, y.shape)
print("Resampled dataset shape:", X_resampled_kmean.shape, y_resampled_kmean.shape)

# Instantiate the SVMSMOTE oversampler
svm_smote = SVMSMOTE(random_state=42)

# Apply SVMSMOTE to the dataset
X_resampled_svm, y_resampled_svm = svm_smote.fit_resample(X, y)
# Print the resampled data
print("Original dataset shape:", X.shape, y.shape)
print("Resampled dataset shape:", X_resampled_svm.shape, y_resampled_svm.shape)

# Instantiate the Borderline SMOTE oversampler
borderline_smote = BorderlineSMOTE(random_state=42)

# Apply Borderline SMOTE to the dataset
X_resampled_border, y_resampled_border = borderline_smote.fit_resample(X, y)
print("Original dataset shape:", X.shape, y.shape)
print("Resampled dataset shape:", X_resampled_border.shape, y_resampled_border.shape)

# Instantiate the ADASYN oversampler
adasyn = ADASYN(random_state=42)

# Apply ADASYN to the dataset
X_resampled_ad, y_resampled_ad = adasyn.fit_resample(X, y)
print("Original dataset shape:", X.shape, y.shape)
print("Resampled dataset shape:", X_resampled_ad.shape, y_resampled_ad.shape)

# Split the data into train and test sets
X_train_smote, X_test_smote, y_train_smote, y_test_smote = train_test_split(
    X_resampled_smote, y_resampled_smote, test_size=0.3, random_state=42
)

# Split the data into train and test sets
X_train_kmean, X_test_kmean, y_train_kmean, y_test_kmean = train_test_split(
    X_resampled_kmean, y_resampled_kmean, test_size=0.3, random_state=42
)

# Split the data into train and test sets
X_train_border, X_test_border, y_train_border, y_test_border = train_test_split(
    X_resampled_border, y_resampled_border, test_size=0.3, random_state=42
)

# Split the data into train and test sets
X_train_ad, X_test_ad, y_train_ad, y_test_ad = train_test_split(
    X_resampled_ad, y_resampled_ad, test_size=0.3, random_state=42
)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

datasets = [
    ('SMOTE', X_train_smote, y_train_smote, X_test, y_test),
    ('K-Means SMOTE', X_train_kmean, y_train_kmean, X_test, y_test),
    ('Borderline SMOTE', X_train_border, y_train_border, X_test, y_test),
    ('ADASYN', X_train_ad, y_train_ad, X_test, y_test),
    ('Without Oversampling', X_train, y_train, X_test, y_test),
]

from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
# from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate

from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
# from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate

Results = [['Name', 'Tree', 'Depth', 'Fold1', 'Fold2', 'Fold3', 'Fold4', 'Fold5', 'CV']]
n_estimators = [50, 100, 200]
max_depth = [50, 100, 200]

for i in range(5):

  name, X_train, y_train, X_test, y_test = datasets[i]

  for j in n_estimators:
    for k in max_depth:

      if k<j:
        continue

      model = MLPClassifier(hidden_layer_sizes=(j, k), max_iter=100, solver='adam', random_state=42)

      scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
      }

      cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)
      R = cv_results['train_f1']

      Results.append([name, j, k, R[0], R[1], R[2], R[3], R[4], np.mean(R)])

print(tabulate(Results, headers='firstrow', tablefmt='pipe'))

print(tabulate(Results, headers='firstrow', tablefmt='pipe'))

# Initialize dictionary to store max F1 scores and corresponding j and k values for each dataset
max_f1_values = {}

# Iterate over datasets
for name, _, _, _, _ in datasets:
    # name='SMOTE'
    # Filter relevant rows from Results list based on dataset name
    dataset_results = [result for result in Results[1:] if result[0] == name]

    dataset_results_array = np.array(dataset_results)
    max_indices = np.argmax(dataset_results_array[:,3:], axis=0)
    print("______________________________________")
    for i, max_index in enumerate(max_indices):
        print(f"{name} Data {i + 1}: Parameters {dataset_results_array[max_index,1],dataset_results_array[max_index,2]}")

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate



# Function to perform cross-validation and collect results
def perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth):
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

    # Cross-validation with macro-averaged metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
    }

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Model training on the full training set
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    # Predictions on the test set
    y_pred_test = model.predict(X_test)

    # Calculate metrics for the test set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, average='macro')
    test_recall = recall_score(y_test, y_pred_test, average='macro')
    test_f1 = f1_score(y_test, y_pred_test, average='macro')

    conf_matrix_train = confusion_matrix(y_train, y_pred_train)

    # Display confusion matrix
    print(name+" Confusion Matrix Train:")
    print(conf_matrix_train)
    # Calculate accuracy per class
    class_accuracy_train = conf_matrix_train.diagonal() / conf_matrix_train.sum(axis=1)


    conf_matrix = confusion_matrix(y_test, y_pred_test)

    # Display confusion matrix
    print(name+" Confusion Matrix Test:")
    print(conf_matrix)
    # Calculate accuracy per class
    class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)



    # Compile results into a list of dictionaries
    train_results = {
        'Dataset': f"{name} (RandomForest)",
        'Type': 'Train',
        'C0':class_accuracy_train[0],
        'C1':class_accuracy_train[1],
        'C2':class_accuracy_train[2],
        'C3':class_accuracy_train[3],
        'Accuracy': np.mean(cv_results['train_accuracy']),
        'Precision': np.mean(cv_results['train_precision']),
        'Recall': np.mean(cv_results['train_recall']),
        'F1 Score': np.mean(cv_results['train_f1'])
    }

    test_results = {
        'Dataset': f"{name} (RandomForest)",
        'Type': 'Test',
        'C0':class_accuracy[0],
        'C1':class_accuracy[1],
        'C2':class_accuracy[2],
        'C3':class_accuracy[3],
        'Accuracy': test_accuracy,
        'Precision': test_precision,
        'Recall': test_recall,
        'F1 Score': test_f1
    }

    return [train_results, test_results]

# Create an empty list to store results
all_results = []

# Loop through the datasets and perform cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
  if name=='SMOTE':
    n_estimators, max_depth = 80, 20
  if name=='K-Means SMOTE':
    n_estimators, max_depth = 80, 20
  if name=='Borderline SMOTE':
    n_estimators, max_depth = 80, 20
  if name=='ADASYN':
    n_estimators, max_depth = 80, 20
  if name=='Without Oversampling':
    n_estimators, max_depth = 80, 20


  results = perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth)
  all_results.extend(results)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

datasets

from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate

# Function to perform cross-validation and collect results
def perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth):
    model = AdaBoostClassifier(n_estimators=n_estimators, learning_rate=max_depth, random_state=42)  # You can adjust the number of estimators

    # Cross-validation with macro-averaged metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
    }

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Model training on the full training set
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    # Predictions on the test set
    y_pred_test = model.predict(X_test)

    # Calculate metrics for the test set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, average='macro')
    test_recall = recall_score(y_test, y_pred_test, average='macro')
    test_f1 = f1_score(y_test, y_pred_test, average='macro')

    conf_matrix_train = confusion_matrix(y_train, y_pred_train)

    # Display confusion matrix
    print(name+" Confusion Matrix Train:")
    print(conf_matrix_train)
    # Calculate accuracy per class
    class_accuracy_train = conf_matrix_train.diagonal() / conf_matrix_train.sum(axis=1)


    conf_matrix = confusion_matrix(y_test, y_pred_test)

    # Display confusion matrix
    print(name+" Confusion Matrix Test:")
    print(conf_matrix)
    # Calculate accuracy per class
    class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)



    # Compile results into a list of dictionaries
    train_results = {
        'Dataset': f"{name} (AdaBoost)",
        'Type': 'Train',
        'C0':class_accuracy_train[0],
        'C1':class_accuracy_train[1],
        'C2':class_accuracy_train[2],
        'C3':class_accuracy_train[3],
        'Accuracy': np.mean(cv_results['train_accuracy']),
        'Precision': np.mean(cv_results['train_precision']),
        'Recall': np.mean(cv_results['train_recall']),
        'F1 Score': np.mean(cv_results['train_f1'])
    }

    test_results = {
        'Dataset': f"{name} (AdaBoost)",
        'Type': 'Test',
        'C0':class_accuracy[0],
        'C1':class_accuracy[1],
        'C2':class_accuracy[2],
        'C3':class_accuracy[3],
        'Accuracy': test_accuracy,
        'Precision': test_precision,
        'Recall': test_recall,
        'F1 Score': test_f1
    }

    return [train_results, test_results]

  # Create an empty list to store results
all_results = []

  # Loop through the datasets and perform cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
  if name=='SMOTE':
    n_estimators, max_depth = 80, 0.5
  if name=='K-Means SMOTE':
    n_estimators, max_depth = 80, 0.5
  if name=='Borderline SMOTE':
    n_estimators, max_depth = 80, 0.5
  if name=='ADASYN':
    n_estimators, max_depth = 80, 0.5
  if name=='Without Oversampling':
    n_estimators, max_depth = 50, 0.9


  results = perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth)
  all_results.extend(results)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

from xgboost import XGBClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate

# Function to perform cross-validation and collect results
def perform_cross_validation(name, X_train, y_train, X_test, y_test, j, k):
    model = XGBClassifier(n_estimators=j, max_depth=k, random_state=42)  # You can adjust the number of estimators

    # Cross-validation with macro-averaged metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
    }

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Model training on the full training set
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    # Predictions on the test set
    y_pred_test = model.predict(X_test)

    # Calculate metrics for the test set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, average='macro')
    test_recall = recall_score(y_test, y_pred_test, average='macro')
    test_f1 = f1_score(y_test, y_pred_test, average='macro')

    conf_matrix_train = confusion_matrix(y_train, y_pred_train)

    # Display confusion matrix
    print(name+" Confusion Matrix Train:")
    print(conf_matrix_train)
    # Calculate accuracy per class
    class_accuracy_train = conf_matrix_train.diagonal() / conf_matrix_train.sum(axis=1)


    conf_matrix = confusion_matrix(y_test, y_pred_test)

    # Display confusion matrix
    print(name+" Confusion Matrix Test:")
    print(conf_matrix)
    # Calculate accuracy per class
    class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)



    # Compile results into a list of dictionaries
    train_results = {
        'Dataset': f"{name} (XGBoost)",
        'Type': 'Train',
        'C0':class_accuracy_train[0],
        'C1':class_accuracy_train[1],
        'C2':class_accuracy_train[2],
        'C3':class_accuracy_train[3],
        'Accuracy': np.mean(cv_results['train_accuracy']),
        'Precision': np.mean(cv_results['train_precision']),
        'Recall': np.mean(cv_results['train_recall']),
        'F1 Score': np.mean(cv_results['train_f1'])
    }

    test_results = {
        'Dataset': f"{name} (XGBoost)",
        'Type': 'Test',
        'C0':class_accuracy[0],
        'C1':class_accuracy[1],
        'C2':class_accuracy[2],
        'C3':class_accuracy[3],
        'Accuracy': test_accuracy,
        'Precision': test_precision,
        'Recall': test_recall,
        'F1 Score': test_f1
    }

    return [train_results, test_results]

  # Create an empty list to store results
all_results = []

  # Loop through the datasets and perform cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
  if name=='SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='K-Means SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='Borderline SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='ADASYN':
    n_estimators, max_depth = 50, 20
  if name=='Without Oversampling':
    n_estimators, max_depth = 50, 10


  results = perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth)
  all_results.extend(results)
# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate

# Function to perform cross-validation and collect results
def perform_cross_validation(name, X_train, y_train, X_test, y_test, j, k):
    model = LGBMClassifier(n_estimators=j, max_depth=k, random_state=42)  # You can adjust the number of estimators

    # Cross-validation with macro-averaged metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
    }

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Model training on the full training set
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    # Predictions on the test set
    y_pred_test = model.predict(X_test)

    # Calculate metrics for the test set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, average='macro')
    test_recall = recall_score(y_test, y_pred_test, average='macro')
    test_f1 = f1_score(y_test, y_pred_test, average='macro')

    conf_matrix_train = confusion_matrix(y_train, y_pred_train)

    # Display confusion matrix
    print(name+" Confusion Matrix Train:")
    print(conf_matrix_train)
    # Calculate accuracy per class
    class_accuracy_train = conf_matrix_train.diagonal() / conf_matrix_train.sum(axis=1)


    conf_matrix = confusion_matrix(y_test, y_pred_test)

    # Display confusion matrix
    print(name+" Confusion Matrix Test:")
    print(conf_matrix)
    # Calculate accuracy per class
    class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)



    # Compile results into a list of dictionaries
    train_results = {
        'Dataset': f"{name} (LGBM)",
        'Type': 'Train',
        'C0':class_accuracy_train[0],
        'C1':class_accuracy_train[1],
        'C2':class_accuracy_train[2],
        'C3':class_accuracy_train[3],
        'Accuracy': np.mean(cv_results['train_accuracy']),
        'Precision': np.mean(cv_results['train_precision']),
        'Recall': np.mean(cv_results['train_recall']),
        'F1 Score': np.mean(cv_results['train_f1'])
    }

    test_results = {
        'Dataset': f"{name} (LGBM)",
        'Type': 'Test',
        'C0':class_accuracy[0],
        'C1':class_accuracy[1],
        'C2':class_accuracy[2],
        'C3':class_accuracy[3],
        'Accuracy': test_accuracy,
        'Precision': test_precision,
        'Recall': test_recall,
        'F1 Score': test_f1
    }

    return [train_results, test_results]

  # Create an empty list to store results
all_results = []

  # Loop through the datasets and perform cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
  if name=='SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='K-Means SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='Borderline SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='ADASYN':
    n_estimators, max_depth = 50, 20
  if name=='Without Oversampling':
    n_estimators, max_depth = 50, 20


  results = perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth)
  all_results.extend(results)
# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

!pip install catboost

from catboost import CatBoostClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from tabulate import tabulate

# Function to perform cross-validation and collect results
def perform_cross_validation(name, X_train, y_train, X_test, y_test, j, k):
    model = CatBoostClassifier(
        n_estimators=j,
        max_depth=k,
        random_state=42,
        task_type="GPU",  # Specify GPU as the task type
        verbose=0
    )

    # Cross-validation with macro-averaged metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
    }

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Model training on the full training set
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    # Predictions on the test set
    y_pred_test = model.predict(X_test)

    # Calculate metrics for the test set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, average='macro')
    test_recall = recall_score(y_test, y_pred_test, average='macro')
    test_f1 = f1_score(y_test, y_pred_test, average='macro')

    conf_matrix_train = confusion_matrix(y_train, y_pred_train)

    # Display confusion matrix
    print(name+" Confusion Matrix Train:")
    print(conf_matrix_train)
    # Calculate accuracy per class
    class_accuracy_train = conf_matrix_train.diagonal() / conf_matrix_train.sum(axis=1)


    conf_matrix = confusion_matrix(y_test, y_pred_test)

    # Display confusion matrix
    print(name+" Confusion Matrix Test:")
    print(conf_matrix)
    # Calculate accuracy per class
    class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)



    # Compile results into a list of dictionaries
    train_results = {
        'Dataset': f"{name} (CatBoost)",
        'Type': 'Train',
        'C0':class_accuracy_train[0],
        'C1':class_accuracy_train[1],
        'C2':class_accuracy_train[2],
        'C3':class_accuracy_train[3],
        'Accuracy': np.mean(cv_results['train_accuracy']),
        'Precision': np.mean(cv_results['train_precision']),
        'Recall': np.mean(cv_results['train_recall']),
        'F1 Score': np.mean(cv_results['train_f1'])
    }

    test_results = {
        'Dataset': f"{name} (CatBoost)",
        'Type': 'Test',
        'C0':class_accuracy[0],
        'C1':class_accuracy[1],
        'C2':class_accuracy[2],
        'C3':class_accuracy[3],
        'Accuracy': test_accuracy,
        'Precision': test_precision,
        'Recall': test_recall,
        'F1 Score': test_f1
    }

    return [train_results, test_results]

  # Create an empty list to store results
all_results = []

  # Loop through the datasets and perform cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
  if name=='SMOTE':
    n_estimators, max_depth = 50, 10
  if name=='K-Means SMOTE':
    n_estimators, max_depth = 50, 10
  if name=='Borderline SMOTE':
    n_estimators, max_depth = 50, 10
  if name=='ADASYN':
    n_estimators, max_depth = 50, 10
  if name=='Without Oversampling':
    n_estimators, max_depth = 50, 10


  results = perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth)
  all_results.extend(results)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from tabulate import tabulate

# Function to perform cross-validation and collect results
def perform_cross_validation(name, X_train, y_train, X_test, y_test, j, k):
    model = MLPClassifier(hidden_layer_sizes=(j, k), max_iter=100, solver='adam', random_state=42)
    # Adjust the hidden_layer_sizes and other parameters based on your requirements

    # Cross-validation with macro-averaged metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro')
    }

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Model training on the full training set
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    # Predictions on the test set
    y_pred_test = model.predict(X_test)

    # Calculate metrics for the test set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, average='macro')
    test_recall = recall_score(y_test, y_pred_test, average='macro')
    test_f1 = f1_score(y_test, y_pred_test, average='macro')

    conf_matrix_train = confusion_matrix(y_train, y_pred_train)

    # Display confusion matrix
    print(name+" Confusion Matrix Train:")
    print(conf_matrix_train)
    # Calculate accuracy per class
    class_accuracy_train = conf_matrix_train.diagonal() / conf_matrix_train.sum(axis=1)


    conf_matrix = confusion_matrix(y_test, y_pred_test)

    # Display confusion matrix
    print(name+" Confusion Matrix Test:")
    print(conf_matrix)
    # Calculate accuracy per class
    class_accuracy = conf_matrix.diagonal() / conf_matrix.sum(axis=1)



    # Compile results into a list of dictionaries
    train_results = {
        'Dataset': f"{name} (MLP)",
        'Type': 'Train',
        'C0':class_accuracy_train[0],
        'C1':class_accuracy_train[1],
        'C2':class_accuracy_train[2],
        'C3':class_accuracy_train[3],
        'Accuracy': np.mean(cv_results['train_accuracy']),
        'Precision': np.mean(cv_results['train_precision']),
        'Recall': np.mean(cv_results['train_recall']),
        'F1 Score': np.mean(cv_results['train_f1'])
    }

    test_results = {
        'Dataset': f"{name} (MLP)",
        'Type': 'Test',
        'C0':class_accuracy[0],
        'C1':class_accuracy[1],
        'C2':class_accuracy[2],
        'C3':class_accuracy[3],
        'Accuracy': test_accuracy,
        'Precision': test_precision,
        'Recall': test_recall,
        'F1 Score': test_f1
    }

    return [train_results, test_results]

  # Create an empty list to store results
all_results = []

  # Loop through the datasets and perform cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
  if name=='SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='K-Means SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='Borderline SMOTE':
    n_estimators, max_depth = 50, 20
  if name=='ADASYN':
    n_estimators, max_depth = 50, 20
  if name=='Without Oversampling':
    n_estimators, max_depth = 50, 10


  results = perform_cross_validation(name, X_train, y_train, X_test, y_test, n_estimators, max_depth)
  all_results.extend(results)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

y_test.shape

datasets_lstm = [
    ('SMOTE', X_train_smote.reshape(-1,5,11), y_train_smote, X_test.reshape(-1,5,11), y_test),
    ('K-Means SMOTE', X_train_kmean.reshape(-1,5,11), y_train_kmean, X_test.reshape(-1,5,11), y_test),
    ('Borderline SMOTE', X_train_border.reshape(-1,5,11), y_train_border, X_test.reshape(-1,5,11), y_test),
    ('ADASYN', X_train_ad.reshape(-1,5,11), y_train_ad, X_test.reshape(-1,5,11), y_test),
    ('Without Oversampling', X_train.reshape(-1,5,11), y_train, X_test.reshape(-1,5,11), y_test),
]

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
from tabulate import tabulate
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

# Function to create and train LSTM model with cross-validation
def train_lstm_model_with_cv(X, y, X_test1, y_test1, name, n_splits=5, epochs=50, batch_size=1024):
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    y_categorical = to_categorical(y_encoded)

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    all_results = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y_categorical[train_index], y_categorical[test_index]

        model = Sequential()
        model.add(LSTM(50, input_shape=( 5,11)))
        model.add(Dense(4, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        X_train_reshaped = X_train
        X_test_reshaped = X_test

        # Train the model
        model.fit(X_train_reshaped, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=0)

        # Training predictions and metrics
        y_pred_train = np.argmax(model.predict(X_train_reshaped), axis=1)
        train_accuracy = accuracy_score(np.argmax(y_train, axis=1), y_pred_train)
        train_precision = precision_score(np.argmax(y_train, axis=1), y_pred_train, average='macro')
        train_recall = recall_score(np.argmax(y_train, axis=1), y_pred_train, average='macro')
        train_f1 = f1_score(np.argmax(y_train, axis=1), y_pred_train, average='macro')



        # Compile results into a list of dictionaries
        results = {
            'Dataset': f"{name} (LSTM)",
            'Type': 'Train',
            'Accuracy': train_accuracy,
            'Precision': train_precision,
            'Recall': train_recall,
            'F1 Score': train_f1
        }
        all_results.append(results)

    mean_results = {
        'Dataset': f"{name} (LSTM)",
        'Type': 'Train',
        'Accuracy': np.mean([result['Accuracy'] for result in all_results]),
        'Precision': np.mean([result['Precision'] for result in all_results]),
        'Recall': np.mean([result['Recall'] for result in all_results]),
        'F1 Score': np.mean([result['F1 Score'] for result in all_results]),
    }

    # Testing predictions and metrics
    y_pred_test = np.argmax(model.predict(X_test1), axis=1)
    test_accuracy = accuracy_score(y_test1, y_pred_test)
    test_precision = precision_score(y_test1, y_pred_test, average='macro')
    test_recall = recall_score(y_test1, y_pred_test, average='macro')
    test_f1 = f1_score(y_test1, y_pred_test, average='macro')
    results_test = {
            'Dataset': f"{name} (LSTM)",
            'Type': 'Test',
            'Accuracy': test_accuracy,
            'Precision': test_precision,
            'Recall': test_recall,
            'F1 Score': test_f1
        }

    return [mean_results, results_test]

# Create an empty list to store results
all_results = []

# Loop through the datasets and perform LSTM training with cross-validation
for name, X_train, y_train, X_test, y_test in datasets_lstm:
    print(1)
    results = train_lstm_model_with_cv(X_train, y_train, X_test, y_test, name)
    all_results.extend(results)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
from tabulate import tabulate

# Define the classifiers for ensembling
classifiers = [
    RandomForestClassifier(random_state=42),
    XGBClassifier(random_state=42),
    CatBoostClassifier(random_state=42, verbose=False),
    LGBMClassifier(random_state=42),
    AdaBoostClassifier(random_state=42),
]

# Provided dataset
datasets = [
    ('SMOTE', X_train_smote, y_train_smote, X_test, y_test),
    ('K-Means SMOTE', X_train_kmean, y_train_kmean, X_test, y_test),
    ('Borderline SMOTE', X_train_border, y_train_border, X_test, y_test),
    ('ADASYN', X_train_ad, y_train_ad, X_test, y_test),
    ('Without Oversampling', X_train, y_train, X_test, y_test),
]

# Function to perform dynamic ensembling with cross-validation
def perform_dynamic_ensembling(name, X_train, y_train, X_test, y_test, classifiers):
    predictions = []

    # Train the classifiers individually
    for clf in classifiers:
        clf.fit(X_train, y_train)

    # Perform predictions with each classifier
    predictions = []
    for clf in classifiers:
        clf_predictions = clf.predict(X_test)
        predictions.append(clf_predictions)

    # Dynamic ensemble
    ensemble_predictions = []
    for i in range(len(X_test)):
        votes = {}  # Dictionary to store the votes for each class label
        for clf_index, clf in enumerate(classifiers):
            clf_prediction = predictions[clf_index][i]
            if isinstance(clf_prediction, np.int64) or isinstance(clf_prediction, np.float64):
                clf_prediction = [clf_prediction]  # Convert numpy.int64 or numpy.float64 to list
            clf_prediction_tuple = tuple(clf_prediction)
            if clf_prediction_tuple in votes:
                votes[clf_prediction_tuple] += 1
            else:
                votes[clf_prediction_tuple] = 1

        # Select the class label with the maximum votes
        ensemble_prediction = max(votes, key=votes.get)
        ensemble_predictions.append(ensemble_prediction)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='macro')
    recall = recall_score(y_test, ensemble_predictions, average='macro')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='macro')

    # Compile results into a list of dictionaries
    results = {
        'Dataset': f"{name} (Dynamic Ensemble)",
        'Type': 'Ensemble',
        'Accuracy': ensemble_accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1_score_a
    }

    return results, ensemble_predictions, y_test

# Create an empty list to store results
all_results = []
R=[]
Y=[]

# Loop through the datasets and perform dynamic ensembling with cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
    results,rr, yy = perform_dynamic_ensembling(name, X_train, y_train, X_test.reshape(-1,55), y_test, classifiers)
    all_results.append(results)
    R.append(rr)
    Y.append(yy)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

R

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
from tabulate import tabulate

# Define the classifiers for ensembling
random_seed = 42

# RandomForestClassifier
rf_classifier = RandomForestClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of trees in the forest
    max_depth=5,  # Maximum depth of the tree
    min_samples_split=2,  # Minimum number of samples required to split an internal node
    min_samples_leaf=1,  # Minimum number of samples required to be at a leaf node
    max_features='auto',  # Number of features to consider when looking for the best split
)

# XGBClassifier
xgb_classifier = XGBClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of boosting rounds
    max_depth=3,  # Maximum depth of a tree
    learning_rate=0.1,  # Step size shrinkage to prevent overfitting
    subsample=1.0,  # Fraction of samples used for fitting the trees
    colsample_bytree=1.0,  # Fraction of features used for fitting the trees
)

# CatBoostClassifier
catboost_classifier = CatBoostClassifier(
    random_state=random_seed,
    iterations=10,  # Number of boosting iterations
    depth=6,  # Depth of the tree
    learning_rate=0.1,  # Step size shrinkage to prevent overfitting
    verbose=False,  # Set to True for verbose output
)

# LGBMClassifier
lgbm_classifier = LGBMClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of boosting rounds
    max_depth=-1,  # Maximum depth of a tree
    learning_rate=0.1,  # Step size shrinkage to prevent overfitting
    subsample=1.0,  # Fraction of samples used for fitting the trees
    colsample_bytree=1.0,  # Fraction of features used for fitting the trees
)

# AdaBoostClassifier
adaboost_classifier = AdaBoostClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of weak learners to train iteratively
    learning_rate=1.0,  # Weight applied to each weak learner
)

# List of classifiers with set hyperparameters
classifiers = [
    rf_classifier,
    xgb_classifier,
    catboost_classifier,
    lgbm_classifier,
    adaboost_classifier,
]

classifiers = [
    RandomForestClassifier(random_state=42),
    XGBClassifier(random_state=42),
    CatBoostClassifier(random_state=42, verbose=False),
    LGBMClassifier(random_state=42),
    AdaBoostClassifier(random_state=42),
]

# Provided dataset
datasets = [
    ('SMOTE', X_train_smote, y_train_smote, X_test, y_test),
    ('K-Means SMOTE', X_train_kmean, y_train_kmean, X_test, y_test),
    ('Borderline SMOTE', X_train_border, y_train_border, X_test, y_test),
    ('ADASYN', X_train_ad, y_train_ad, X_test, y_test),
    ('Without Oversampling', X_train, y_train, X_test, y_test),
]

# Function to perform dynamic ensembling with cross-validation
def perform_dynamic_ensembling(name, X_train, y_train, X_test, y_test, classifiers):
    predictions = []

    # Train the classifiers individually
    for clf in classifiers:
        clf.fit(X_train, y_train)

    # Perform predictions with each classifier
    predictions = []
    for clf in classifiers:
        clf_predictions = clf.predict(X_test)
        predictions.append(clf_predictions)

    # Dynamic ensemble
    ensemble_predictions = []
    for i in range(len(X_test)):
        votes = {}  # Dictionary to store the votes for each class label
        for clf_index, clf in enumerate(classifiers):
            clf_prediction = predictions[clf_index][i]
            if isinstance(clf_prediction, np.int64) or isinstance(clf_prediction, np.float64):
                clf_prediction = [clf_prediction]  # Convert numpy.int64 or numpy.float64 to list
            clf_prediction_tuple = tuple(clf_prediction)
            if clf_prediction_tuple in votes:
                votes[clf_prediction_tuple] += 1
            else:
                votes[clf_prediction_tuple] = 1

        # Select the class label with the maximum votes
        ensemble_prediction = max(votes, key=votes.get)
        ensemble_predictions.append(ensemble_prediction)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='macro')
    recall = recall_score(y_test, ensemble_predictions, average='macro')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='macro')

    # Train predictions and metrics
    train_predictions = []
    for clf in classifiers:
        clf_train_predictions = clf.predict(X_train)
        train_predictions.append(clf_train_predictions)

    train_ensemble_predictions = []
    for i in range(len(X_train)):
        votes = {}  # Dictionary to store the votes for each class label
        for clf_index, clf in enumerate(classifiers):
            clf_prediction = train_predictions[clf_index][i]
            if isinstance(clf_prediction, np.int64) or isinstance(clf_prediction, np.float64):
                clf_prediction = [clf_prediction]  # Convert numpy.int64 or numpy.float64 to list
            clf_prediction_tuple = tuple(clf_prediction)
            if clf_prediction_tuple in votes:
                votes[clf_prediction_tuple] += 1
            else:
                votes[clf_prediction_tuple] = 1

        # Select the class label with the maximum votes
        ensemble_prediction = max(votes, key=votes.get)
        train_ensemble_predictions.append(ensemble_prediction)

    # Evaluate the performance of the ensemble model on the train set
    train_ensemble_accuracy = accuracy_score(y_train, train_ensemble_predictions)
    train_precision = precision_score(y_train, train_ensemble_predictions, average='macro')
    train_recall = recall_score(y_train, train_ensemble_predictions, average='macro')
    train_f1_score = f1_score(y_train, train_ensemble_predictions, average='macro')

    # Compile results into a list of dictionaries
    results = {
        'Dataset': name,
        'Type': 'Test',
        'Accuracy': ensemble_accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1_score_a
    }

    results_train = {
        'Dataset': name,
        'Type': 'Train',
        'Accuracy': train_ensemble_accuracy,
        'Precision': train_precision,
        'Recall': train_recall,
        'F1 Score': train_f1_score
    }

    return [results_train, results]

# Create an empty list to store results

all_results = []

# Loop through the datasets and perform dynamic ensembling with cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
    results = perform_dynamic_ensembling(name, X_train, y_train, X_test.reshape(-1,55), y_test, classifiers)
    all_results.extend(results)


# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)


# Display the results table using tabulate

print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))

!pip install catboost

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
from tabulate import tabulate

# Define the classifiers for ensembling
random_seed = 42

# RandomForestClassifier
rf_classifier = RandomForestClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of trees in the forest
    max_depth=5,  # Maximum depth of the tree
    min_samples_split=2,  # Minimum number of samples required to split an internal node
    min_samples_leaf=1,  # Minimum number of samples required to be at a leaf node
    max_features='auto',  # Number of features to consider when looking for the best split
)

# XGBClassifier
xgb_classifier = XGBClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of boosting rounds
    max_depth=3,  # Maximum depth of a tree
    learning_rate=0.1,  # Step size shrinkage to prevent overfitting
    subsample=1.0,  # Fraction of samples used for fitting the trees
    colsample_bytree=1.0,  # Fraction of features used for fitting the trees
)

# CatBoostClassifier
catboost_classifier = CatBoostClassifier(
    random_state=random_seed,
    iterations=10,  # Number of boosting iterations
    depth=6,  # Depth of the tree
    learning_rate=0.1,  # Step size shrinkage to prevent overfitting
    verbose=False,  # Set to True for verbose output
)

# LGBMClassifier
lgbm_classifier = LGBMClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of boosting rounds
    max_depth=-1,  # Maximum depth of a tree
    learning_rate=0.1,  # Step size shrinkage to prevent overfitting
    subsample=1.0,  # Fraction of samples used for fitting the trees
    colsample_bytree=1.0,  # Fraction of features used for fitting the trees
)

# AdaBoostClassifier
adaboost_classifier = AdaBoostClassifier(
    random_state=random_seed,
    n_estimators=10,  # Number of weak learners to train iteratively
    learning_rate=1.0,  # Weight applied to each weak learner
)

# List of classifiers with set hyperparameters
classifiers = [
    rf_classifier,
    xgb_classifier,
    catboost_classifier,
    lgbm_classifier,
    adaboost_classifier,
]
classifiers = [
    RandomForestClassifier(random_state=42),
    XGBClassifier(random_state=42),
    CatBoostClassifier(random_state=42, verbose=False),
    LGBMClassifier(random_state=42),
    AdaBoostClassifier(random_state=42),
]
# Provided dataset
datasets = [
    ('SMOTE', X_train_smote, y_train_smote, X_test, y_test),
    ('K-Means SMOTE', X_train_kmean, y_train_kmean, X_test, y_test),
    ('Borderline SMOTE', X_train_border, y_train_border, X_test, y_test),
    ('ADASYN', X_train_ad, y_train_ad, X_test, y_test),
    ('Without Oversampling', X_train, y_train, X_test, y_test),
]

# Function to perform dynamic ensembling with cross-validation
def perform_dynamic_ensembling(name, X_train, y_train, X_test, y_test, classifiers):
    predictions_train = []

    # Train the classifiers individually using cross-validation
    for clf in classifiers:
        clf_train_predictions = cross_val_predict(clf, X_train, y_train, cv=5)
        predictions_train.append(clf_train_predictions)

    # Fit the classifiers on the entire training set
    for clf in classifiers:
        clf.fit(X_train, y_train)

    # Perform predictions with each classifier on the test set
    predictions_test = []
    for clf in classifiers:
        clf_test_predictions = clf.predict(X_test)
        predictions_test.append(clf_test_predictions)

    # Dynamic ensemble on the test set
    ensemble_predictions_test = []
    for i in range(len(X_test)):
        votes = {}  # Dictionary to store the votes for each class label
        for clf_index, clf in enumerate(classifiers):
            clf_prediction = predictions_test[clf_index][i]
            if isinstance(clf_prediction, np.int64) or isinstance(clf_prediction, np.float64):
                clf_prediction = [clf_prediction]  # Convert numpy.int64 or numpy.float64 to list
            clf_prediction_tuple = tuple(clf_prediction)
            if clf_prediction_tuple in votes:
                votes[clf_prediction_tuple] += 1
            else:
                votes[clf_prediction_tuple] = 1

        # Select the class label with the maximum votes
        ensemble_prediction = max(votes, key=votes.get)
        ensemble_predictions_test.append(ensemble_prediction)

    # Evaluate the performance of the ensemble model on the test set
    ensemble_accuracy_test = accuracy_score(y_test, ensemble_predictions_test)
    precision_test = precision_score(y_test, ensemble_predictions_test, average='macro')
    recall_test = recall_score(y_test, ensemble_predictions_test, average='macro')
    f1_score_test = f1_score(y_test, ensemble_predictions_test, average='macro')

    # Dynamic ensemble on the train set
    ensemble_predictions_train = []
    for i in range(len(X_train)):
        votes = {}  # Dictionary to store the votes for each class label
        for clf_index, clf in enumerate(classifiers):
            clf_prediction = predictions_train[clf_index][i]
            if isinstance(clf_prediction, np.int64) or isinstance(clf_prediction, np.float64):
                clf_prediction = [clf_prediction]  # Convert numpy.int64 or numpy.float64 to list
            clf_prediction_tuple = tuple(clf_prediction)
            if clf_prediction_tuple in votes:
                votes[clf_prediction_tuple] += 1
            else:
                votes[clf_prediction_tuple] = 1

        # Select the class label with the maximum votes
        ensemble_prediction = max(votes, key=votes.get)
        ensemble_predictions_train.append(ensemble_prediction)

    # Evaluate the performance of the ensemble model on the train set
    ensemble_accuracy_train = accuracy_score(y_train, ensemble_predictions_train)
    precision_train = precision_score(y_train, ensemble_predictions_train, average='macro')
    recall_train = recall_score(y_train, ensemble_predictions_train, average='macro')
    f1_score_train = f1_score(y_train, ensemble_predictions_train, average='macro')

    # Compile results into a list of dictionaries
    results_train = {
        'Dataset': name,
        'Type': 'Train',
        'Accuracy': ensemble_accuracy_train,
        'Precision': precision_train,
        'Recall': recall_train,
        'F1 Score': f1_score_train
    }

    results_test = {
        'Dataset': name,
        'Type': 'Test',
        'Accuracy': ensemble_accuracy_test,
        'Precision': precision_test,
        'Recall': recall_test,
        'F1 Score': f1_score_test
    }

    return [results_train, results_test]

# Create an empty list to store results
all_results = []

# Loop through the datasets and perform dynamic ensembling with cross-validation
for name, X_train, y_train, X_test, y_test in datasets:
    results = perform_dynamic_ensembling(name, X_train, y_train, X_test.reshape(-1,55), y_test, classifiers)
    all_results.extend(results)

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(all_results)

# Display the results table using tabulate
print(tabulate(results_df, headers='keys', tablefmt='pipe', showindex=False))



from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Create a Random Forest classifier object
rf_classifier = RandomForestClassifier(random_state=42)

# Define the parameter grid for Random Forest
param_grid = {
    'n_estimators': [45],
    'max_depth': [25],
}

# Perform Grid Search with 5-fold cross-validation
grid_search = GridSearchCV(rf_classifier, param_grid, cv=StratifiedKFold(n_splits=5), scoring='f1_weighted')
grid_search.fit(X_train_smote, y_train_smote)

# Get the best estimator from the search
best_rf_classifier = grid_search.best_estimator_

# Print the best hyperparameters
print("Best Hyperparameters:")
print(grid_search.best_params_)

# Evaluate the performance of the best classifier on the training set
y_pred_train_best = best_rf_classifier.predict(X_train_smote)

# Calculate the training set metrics
accuracy_train_best = accuracy_score(y_train_smote, y_pred_train_best)
precision_train_best = precision_score(y_train_smote, y_pred_train_best, average='weighted')
recall_train_best = recall_score(y_train_smote, y_pred_train_best, average='weighted')
f1_score_train_best = f1_score(y_train_smote, y_pred_train_best, average='weighted')

# Print the training set results
print("\nBest Random Forest Model (based on cross-validation) - Training Set Metrics:")
print(f"Accuracy: {round(accuracy_train_best, 4)}")
print(f"Precision: {round(precision_train_best, 4)}")
print(f"Recall: {round(recall_train_best, 4)}")
print(f"F1 Score: {round(f1_score_train_best, 4)}")

# Evaluate the performance of the best classifier on the test set
y_pred_test_best = best_rf_classifier.predict(X_test_smote)

# Calculate the test set metrics
accuracy_test_best = accuracy_score(y_test_smote, y_pred_test_best)
precision_test_best = precision_score(y_test_smote, y_pred_test_best, average='weighted')
recall_test_best = recall_score(y_test_smote, y_pred_test_best, average='weighted')
f1_score_test_best = f1_score(y_test_smote, y_pred_test_best, average='weighted')

# Print the results
print("\nBest Random Forest Model (based on cross-validation) - Test Set Metrics:")
print(f"Accuracy: {round(accuracy_test_best, 4)}")
print(f"Precision: {round(precision_test_best, 4)}")
print(f"Recall: {round(recall_test_best, 4)}")
print(f"F1 Score: {round(f1_score_test_best, 4)}")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Create a Random Forest classifier object
rf_classifier = RandomForestClassifier(random_state=42)

# Train the classifier on the SMOTE-resampled data
rf_classifier.fit(X_train_smote, y_train_smote)

# Make predictions on the SMOTE train set
y_pred_train_smote = rf_classifier.predict(X_train_smote)

# Make predictions on the SMOTE test set
y_pred_test_smote = rf_classifier.predict(X_test_smote)

# Evaluate the performance of the classifier on SMOTE train and test sets
accuracy_train_smote = accuracy_score(y_train_smote, y_pred_train_smote)
precision_train_smote = precision_score(y_train_smote, y_pred_train_smote, average='weighted')
recall_train_smote = recall_score(y_train_smote, y_pred_train_smote, average='weighted')
f1_score_train_smote = f1_score(y_train_smote, y_pred_train_smote, average='weighted')

accuracy_test_smote = accuracy_score(y_test_smote, y_pred_test_smote)
precision_test_smote = precision_score(y_test_smote, y_pred_test_smote, average='weighted')
recall_test_smote = recall_score(y_test_smote, y_pred_test_smote, average='weighted')
f1_score_test_smote = f1_score(y_test_smote, y_pred_test_smote, average='weighted')

# Train the classifier on the K-Means SMOTE-resampled data
rf_classifier.fit(X_train_kmean, y_train_kmean)

# Make predictions on the K-Means SMOTE train set
y_pred_train_kmean = rf_classifier.predict(X_train_kmean)

# Make predictions on the K-Means SMOTE test set
y_pred_test_kmean = rf_classifier.predict(X_test_kmean)

# Evaluate the performance of the classifier on K-Means SMOTE train and test sets
accuracy_train_kmean = accuracy_score(y_train_kmean, y_pred_train_kmean)
precision_train_kmean = precision_score(y_train_kmean, y_pred_train_kmean, average='weighted')
recall_train_kmean = recall_score(y_train_kmean, y_pred_train_kmean, average='weighted')
f1_score_train_kmean = f1_score(y_train_kmean, y_pred_train_kmean, average='weighted')

accuracy_test_kmean = accuracy_score(y_test_kmean, y_pred_test_kmean)
precision_test_kmean = precision_score(y_test_kmean, y_pred_test_kmean, average='weighted')
recall_test_kmean = recall_score(y_test_kmean, y_pred_test_kmean, average='weighted')
f1_score_test_kmean = f1_score(y_test_kmean, y_pred_test_kmean, average='weighted')

# Train the classifier on the Borderline SMOTE-resampled data
rf_classifier.fit(X_train_border, y_train_border)

# Make predictions on the Borderline SMOTE train set
y_pred_train_border = rf_classifier.predict(X_train_border)


# Make predictions on the Borderline SMOTE test set
y_pred_test_border = rf_classifier.predict(X_test_border)

# Evaluate the performance of the classifier on Borderline SMOTE train and test sets
accuracy_train_border = accuracy_score(y_train_border, y_pred_train_border)
precision_train_border = precision_score(y_train_border, y_pred_train_border, average='weighted')
recall_train_border = recall_score(y_train_border, y_pred_train_border, average='weighted')
f1_score_train_border = f1_score(y_train_border, y_pred_train_border, average='weighted')

accuracy_test_border = accuracy_score(y_test_border, y_pred_test_border)
precision_test_border = precision_score(y_test_border, y_pred_test_border, average='weighted')
recall_test_border = recall_score(y_test_border, y_pred_test_border, average='weighted')
f1_score_test_border = f1_score(y_test_border, y_pred_test_border, average='weighted')

# Train the classifier on the ADASYN-resampled data
rf_classifier.fit(X_train_ad, y_train_ad)

# Make predictions on the ADASYN train set
y_pred_train_ad = rf_classifier.predict(X_train_ad)

# Make predictions on the ADASYN test set
y_pred_test_ad = rf_classifier.predict(X_test_ad)

# Evaluate the performance of the classifier on ADASYN train and test sets
accuracy_train_ad = accuracy_score(y_train_ad, y_pred_train_ad)
precision_train_ad = precision_score(y_train_ad, y_pred_train_ad, average='weighted')
recall_train_ad = recall_score(y_train_ad, y_pred_train_ad, average='weighted')
f1_score_train_ad = f1_score(y_train_ad, y_pred_train_ad, average='weighted')

accuracy_test_ad = accuracy_score(y_test_ad, y_pred_test_ad)
precision_test_ad = precision_score(y_test_ad, y_pred_test_ad, average='weighted')
recall_test_ad = recall_score(y_test_ad, y_pred_test_ad, average='weighted')
f1_score_test_ad = f1_score(y_test_ad, y_pred_test_ad, average='weighted')

# Train the classifier on the original data
rf_classifier.fit(X_train, y_train)

# Make predictions on the original train set
y_pred_train = rf_classifier.predict(X_train)

# Make predictions on the original test set
y_pred_test = rf_classifier.predict(X_test)

# Evaluate the performance of the classifier on the original train and test sets
accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, average='weighted')
recall_train = recall_score(y_train, y_pred_train, average='weighted')
f1_score_train = f1_score(y_train, y_pred_train, average='weighted')

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, average='weighted')
recall_test = recall_score(y_test, y_pred_test, average='weighted')
f1_score_test = f1_score(y_test, y_pred_test, average='weighted')

# Define the performance metrics and their corresponding values
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
results = [
    ["SMOTE (Train)", round(accuracy_train_smote, 4), round(precision_train_smote, 4), round(recall_train_smote, 4), round(f1_score_train_smote, 4)],
    ["SMOTE (Test)", round(accuracy_test_smote, 4), round(precision_test_smote, 4), round(recall_test_smote, 4), round(f1_score_test_smote, 4)],
    ["K-Means SMOTE (Train)", round(accuracy_train_kmean, 4), round(precision_train_kmean, 4), round(recall_train_kmean, 4), round(f1_score_train_kmean, 4)],
    ["K-Means SMOTE (Test)", round(accuracy_test_kmean, 4), round(precision_test_kmean, 4), round(recall_test_kmean, 4), round(f1_score_test_kmean, 4)],
    ["Borderline SMOTE (Train)", round(accuracy_train_border, 4), round(precision_train_border, 4), round(recall_train_border, 4), round(f1_score_train_border, 4)],
    ["Borderline SMOTE (Test)", round(accuracy_test_border, 4), round(precision_test_border, 4), round(recall_test_border, 4), round(f1_score_test_border, 4)],
    ["ADASYN (Train)", round(accuracy_train_ad, 4), round(precision_train_ad, 4), round(recall_train_ad, 4), round(f1_score_train_ad, 4)],
    ["ADASYN (Test)", round(accuracy_test_ad, 4), round(precision_test_ad, 4), round(recall_test_ad, 4), round(f1_score_test_ad, 4)],
    ["Without Oversampling (Train)", round(accuracy_train, 4), round(precision_train, 4), round(recall_train, 4), round(f1_score_train, 4)],
    ["Without Oversampling (Test)", round(accuracy_test, 4), round(precision_test, 4), round(recall_test, 4), round(f1_score_test, 4)]
]


# Print the results in table format
table = tabulate(results, headers=["Random Forest", "Accuracy", "Precision", "Recall", "F1 Score"], tablefmt="presto")
print(table)

#AdaBoost

from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Create an AdaBoost classifier object
adaboost_classifier = AdaBoostClassifier(random_state=42)

# Train the classifier on the SMOTE-resampled data
adaboost_classifier.fit(X_train_smote, y_train_smote)

# Make predictions on the SMOTE train set
y_pred_train_smote = adaboost_classifier.predict(X_train_smote)

# Make predictions on the SMOTE test set
y_pred_test_smote = adaboost_classifier.predict(X_test_smote)

# Evaluate the performance of the classifier on SMOTE train and test sets
accuracy_train_smote = accuracy_score(y_train_smote, y_pred_train_smote)
precision_train_smote = precision_score(y_train_smote, y_pred_train_smote, average='weighted')
recall_train_smote = recall_score(y_train_smote, y_pred_train_smote, average='weighted')
f1_score_train_smote = f1_score(y_train_smote, y_pred_train_smote, average='weighted')

accuracy_test_smote = accuracy_score(y_test_smote, y_pred_test_smote)
precision_test_smote = precision_score(y_test_smote, y_pred_test_smote, average='weighted')
recall_test_smote = recall_score(y_test_smote, y_pred_test_smote, average='weighted')
f1_score_test_smote = f1_score(y_test_smote, y_pred_test_smote, average='weighted')

# Train the classifier on the K-Means SMOTE-resampled data
adaboost_classifier.fit(X_train_kmean, y_train_kmean)

# Make predictions on the K-Means SMOTE train set
y_pred_train_kmean = adaboost_classifier.predict(X_train_kmean)

# Make predictions on the K-Means SMOTE test set
y_pred_test_kmean = adaboost_classifier.predict(X_test_kmean)

# Evaluate the performance of the classifier on K-Means SMOTE train and test sets
accuracy_train_kmean = accuracy_score(y_train_kmean, y_pred_train_kmean)
precision_train_kmean = precision_score(y_train_kmean, y_pred_train_kmean, average='weighted')
recall_train_kmean = recall_score(y_train_kmean, y_pred_train_kmean, average='weighted')
f1_score_train_kmean = f1_score(y_train_kmean, y_pred_train_kmean, average='weighted')

accuracy_test_kmean = accuracy_score(y_test_kmean, y_pred_test_kmean)
precision_test_kmean = precision_score(y_test_kmean, y_pred_test_kmean, average='weighted')
recall_test_kmean = recall_score(y_test_kmean, y_pred_test_kmean, average='weighted')
f1_score_test_kmean = f1_score(y_test_kmean, y_pred_test_kmean, average='weighted')

# Train the classifier on the Borderline SMOTE-resampled data
adaboost_classifier.fit(X_train_border, y_train_border)

# Make predictions on the Borderline SMOTE train set
y_pred_train_border = adaboost_classifier.predict(X_train_border)

# Make predictions on the Borderline SMOTE test set
y_pred_test_border = adaboost_classifier.predict(X_test_border)

# Evaluate the performance of the classifier on Borderline SMOTE train and test sets
accuracy_train_border = accuracy_score(y_train_border, y_pred_train_border)
precision_train_border = precision_score(y_train_border, y_pred_train_border, average='weighted')
recall_train_border = recall_score(y_train_border, y_pred_train_border, average='weighted')
f1_score_train_border = f1_score(y_train_border, y_pred_train_border, average='weighted')

accuracy_test_border = accuracy_score(y_test_border, y_pred_test_border)
precision_test_border = precision_score(y_test_border, y_pred_test_border, average='weighted')
recall_test_border = recall_score(y_test_border, y_pred_test_border, average='weighted')
f1_score_test_border = f1_score(y_test_border, y_pred_test_border, average='weighted')

# Train the classifier on the ADASYN-resampled data
adaboost_classifier.fit(X_train_ad, y_train_ad)

# Make predictions on the ADASYN train set
y_pred_train_ad = adaboost_classifier.predict(X_train_ad)

# Make predictions on the ADASYN test set
y_pred_test_ad = adaboost_classifier.predict(X_test_ad)

# Evaluate the performance of the classifier on ADASYN train and test sets
accuracy_train_ad = accuracy_score(y_train_ad, y_pred_train_ad)
precision_train_ad = precision_score(y_train_ad, y_pred_train_ad, average='weighted')
recall_train_ad = recall_score(y_train_ad, y_pred_train_ad, average='weighted')
f1_score_train_ad = f1_score(y_train_ad, y_pred_train_ad, average='weighted')

accuracy_test_ad = accuracy_score(y_test_ad, y_pred_test_ad)
precision_test_ad = precision_score(y_test_ad, y_pred_test_ad, average='weighted')
recall_test_ad = recall_score(y_test_ad, y_pred_test_ad, average='weighted')
f1_score_test_ad = f1_score(y_test_ad, y_pred_test_ad, average='weighted')

# Train the classifier on the original data
adaboost_classifier.fit(X_train, y_train)

# Make predictions on the original train set
y_pred_train = adaboost_classifier.predict(X_train)

# Make predictions on the original test set
y_pred_test = adaboost_classifier.predict(X_test)

# Evaluate the performance of the classifier on the original train and test sets
accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, average='weighted')
recall_train = recall_score(y_train, y_pred_train, average='weighted')
f1_score_train = f1_score(y_train, y_pred_train, average='weighted')

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, average='weighted')
recall_test = recall_score(y_test, y_pred_test, average='weighted')
f1_score_test = f1_score(y_test, y_pred_test, average='weighted')

# Define the performance metrics and their corresponding values
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
results = [
    ["SMOTE (Train)", round(accuracy_train_smote, 4), round(precision_train_smote, 4), round(recall_train_smote, 4), round(f1_score_train_smote, 4)],
    ["SMOTE (Test)", round(accuracy_test_smote, 4), round(precision_test_smote, 4), round(recall_test_smote, 4), round(f1_score_test_smote, 4)],
    ["K-Means SMOTE (Train)", round(accuracy_train_kmean, 4), round(precision_train_kmean, 4), round(recall_train_kmean, 4), round(f1_score_train_kmean, 4)],
    ["K-Means SMOTE (Test)", round(accuracy_test_kmean, 4), round(precision_test_kmean, 4), round(recall_test_kmean, 4), round(f1_score_test_kmean, 4)],
    ["Borderline SMOTE (Train)", round(accuracy_train_border, 4), round(precision_train_border, 4), round(recall_train_border, 4), round(f1_score_train_border, 4)],
    ["Borderline SMOTE (Test)", round(accuracy_test_border, 4), round(precision_test_border, 4), round(recall_test_border, 4), round(f1_score_test_border, 4)],
    ["ADASYN (Train)", round(accuracy_train_ad, 4), round(precision_train_ad, 4), round(recall_train_ad, 4), round(f1_score_train_ad, 4)],
    ["ADASYN (Test)", round(accuracy_test_ad, 4), round(precision_test_ad, 4), round(recall_test_ad, 4), round(f1_score_test_ad, 4)],
    ["Without Oversampling (Train)", round(accuracy_train, 4), round(precision_train, 4), round(recall_train, 4), round(f1_score_train, 4)],
    ["Without Oversampling (Test)", round(accuracy_test, 4), round(precision_test, 4), round(recall_test, 4), round(f1_score_test, 4)]
]


# Print the results in table format
table = tabulate(results, headers=["AdaBoost", "Accuracy", "Precision", "Recall", "F1 Score"], tablefmt="presto")
print(table)

#CatBoost

!pip install catboost

from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Create an AdaBoost classifier object
catboost_classifier = CatBoostClassifier(random_state=42)

# Train the classifier on the SMOTE-resampled data
catboost_classifier.fit(X_train_smote, y_train_smote)

# Make predictions on the SMOTE train set
y_pred_train_smote = catboost_classifier.predict(X_train_smote)

# Make predictions on the SMOTE test set
y_pred_test_smote = catboost_classifier.predict(X_test_smote)

# Evaluate the performance of the classifier on SMOTE train and test sets
accuracy_train_smote = accuracy_score(y_train_smote, y_pred_train_smote)
precision_train_smote = precision_score(y_train_smote, y_pred_train_smote, average='weighted')
recall_train_smote = recall_score(y_train_smote, y_pred_train_smote, average='weighted')
f1_score_train_smote = f1_score(y_train_smote, y_pred_train_smote, average='weighted')

accuracy_test_smote = accuracy_score(y_test_smote, y_pred_test_smote)
precision_test_smote = precision_score(y_test_smote, y_pred_test_smote, average='weighted')
recall_test_smote = recall_score(y_test_smote, y_pred_test_smote, average='weighted')
f1_score_test_smote = f1_score(y_test_smote, y_pred_test_smote, average='weighted')

# Train the classifier on the K-Means SMOTE-resampled data
catboost_classifier.fit(X_train_kmean, y_train_kmean)

# Make predictions on the K-Means SMOTE train set
y_pred_train_kmean = catboost_classifier.predict(X_train_kmean)

# Make predictions on the K-Means SMOTE test set
y_pred_test_kmean = catboost_classifier.predict(X_test_kmean)

# Evaluate the performance of the classifier on K-Means SMOTE train and test sets
accuracy_train_kmean = accuracy_score(y_train_kmean, y_pred_train_kmean)
precision_train_kmean = precision_score(y_train_kmean, y_pred_train_kmean, average='weighted')
recall_train_kmean = recall_score(y_train_kmean, y_pred_train_kmean, average='weighted')
f1_score_train_kmean = f1_score(y_train_kmean, y_pred_train_kmean, average='weighted')

accuracy_test_kmean = accuracy_score(y_test_kmean, y_pred_test_kmean)
precision_test_kmean = precision_score(y_test_kmean, y_pred_test_kmean, average='weighted')
recall_test_kmean = recall_score(y_test_kmean, y_pred_test_kmean, average='weighted')
f1_score_test_kmean = f1_score(y_test_kmean, y_pred_test_kmean, average='weighted')

# Train the classifier on the Borderline SMOTE-resampled data
catboost_classifier.fit(X_train_border, y_train_border)

# Make predictions on the Borderline SMOTE train set
y_pred_train_border = catboost_classifier.predict(X_train_border)

# Make predictions on the Borderline SMOTE test set
y_pred_test_border = catboost_classifier.predict(X_test_border)

# Evaluate the performance of the classifier on Borderline SMOTE train and test sets
accuracy_train_border = accuracy_score(y_train_border, y_pred_train_border)
precision_train_border = precision_score(y_train_border, y_pred_train_border, average='weighted')
recall_train_border = recall_score(y_train_border, y_pred_train_border, average='weighted')
f1_score_train_border = f1_score(y_train_border, y_pred_train_border, average='weighted')

accuracy_test_border = accuracy_score(y_test_border, y_pred_test_border)
precision_test_border = precision_score(y_test_border, y_pred_test_border, average='weighted')
recall_test_border = recall_score(y_test_border, y_pred_test_border, average='weighted')
f1_score_test_border = f1_score(y_test_border, y_pred_test_border, average='weighted')

# Train the classifier on the ADASYN-resampled data
catboost_classifier.fit(X_train_ad, y_train_ad)

# Make predictions on the ADASYN train set
y_pred_train_ad = catboost_classifier.predict(X_train_ad)

# Make predictions on the ADASYN test set
y_pred_test_ad = catboost_classifier.predict(X_test_ad)

# Evaluate the performance of the classifier on ADASYN train and test sets
accuracy_train_ad = accuracy_score(y_train_ad, y_pred_train_ad)
precision_train_ad = precision_score(y_train_ad, y_pred_train_ad, average='weighted')
recall_train_ad = recall_score(y_train_ad, y_pred_train_ad, average='weighted')
f1_score_train_ad = f1_score(y_train_ad, y_pred_train_ad, average='weighted')

accuracy_test_ad = accuracy_score(y_test_ad, y_pred_test_ad)
precision_test_ad = precision_score(y_test_ad, y_pred_test_ad, average='weighted')
recall_test_ad = recall_score(y_test_ad, y_pred_test_ad, average='weighted')
f1_score_test_ad = f1_score(y_test_ad, y_pred_test_ad, average='weighted')

# Train the classifier on the original data
catboost_classifier.fit(X_train, y_train)

# Make predictions on the original train set
y_pred_train = catboost_classifier.predict(X_train)

# Make predictions on the original test set
y_pred_test = catboost_classifier.predict(X_test)

# Evaluate the performance of the classifier on the original train and test sets
accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, average='weighted')
recall_train = recall_score(y_train, y_pred_train, average='weighted')
f1_score_train = f1_score(y_train, y_pred_train, average='weighted')

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, average='weighted')
recall_test = recall_score(y_test, y_pred_test, average='weighted')
f1_score_test = f1_score(y_test, y_pred_test, average='weighted')

# Define the performance metrics and their corresponding values
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
results = [
    ["SMOTE (Train)", round(accuracy_train_smote, 4), round(precision_train_smote, 4), round(recall_train_smote, 4), round(f1_score_train_smote, 4)],
    ["SMOTE (Test)", round(accuracy_test_smote, 4), round(precision_test_smote, 4), round(recall_test_smote, 4), round(f1_score_test_smote, 4)],
    ["K-Means SMOTE (Train)", round(accuracy_train_kmean, 4), round(precision_train_kmean, 4), round(recall_train_kmean, 4), round(f1_score_train_kmean, 4)],
    ["K-Means SMOTE (Test)", round(accuracy_test_kmean, 4), round(precision_test_kmean, 4), round(recall_test_kmean, 4), round(f1_score_test_kmean, 4)],
    ["Borderline SMOTE (Train)", round(accuracy_train_border, 4), round(precision_train_border, 4), round(recall_train_border, 4), round(f1_score_train_border, 4)],
    ["Borderline SMOTE (Test)", round(accuracy_test_border, 4), round(precision_test_border, 4), round(recall_test_border, 4), round(f1_score_test_border, 4)],
    ["ADASYN (Train)", round(accuracy_train_ad, 4), round(precision_train_ad, 4), round(recall_train_ad, 4), round(f1_score_train_ad, 4)],
    ["ADASYN (Test)", round(accuracy_test_ad, 4), round(precision_test_ad, 4), round(recall_test_ad, 4), round(f1_score_test_ad, 4)],
    ["Without Oversampling (Train)", round(accuracy_train, 4), round(precision_train, 4), round(recall_train, 4), round(f1_score_train, 4)],
    ["Without Oversampling (Test)", round(accuracy_test, 4), round(precision_test, 4), round(recall_test, 4), round(f1_score_test, 4)]
]


# Print the results in table format
table = tabulate(results, headers=["CatBoost", "Accuracy", "Precision", "Recall", "F1 Score"], tablefmt="presto")
print(table)

#XGBoost

from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Create an AdaBoost classifier object
xgb_classifier = XGBClassifier(random_state=42)

# Train the classifier on the SMOTE-resampled data
xgb_classifier.fit(X_train_smote, y_train_smote)

# Make predictions on the SMOTE train set
y_pred_train_smote = xgb_classifier.predict(X_train_smote)

# Make predictions on the SMOTE test set
y_pred_test_smote = xgb_classifier.predict(X_test_smote)

# Evaluate the performance of the classifier on SMOTE train and test sets
accuracy_train_smote = accuracy_score(y_train_smote, y_pred_train_smote)
precision_train_smote = precision_score(y_train_smote, y_pred_train_smote, average='weighted')
recall_train_smote = recall_score(y_train_smote, y_pred_train_smote, average='weighted')
f1_score_train_smote = f1_score(y_train_smote, y_pred_train_smote, average='weighted')

accuracy_test_smote = accuracy_score(y_test_smote, y_pred_test_smote)
precision_test_smote = precision_score(y_test_smote, y_pred_test_smote, average='weighted')
recall_test_smote = recall_score(y_test_smote, y_pred_test_smote, average='weighted')
f1_score_test_smote = f1_score(y_test_smote, y_pred_test_smote, average='weighted')

# Train the classifier on the K-Means SMOTE-resampled data
xgb_classifier.fit(X_train_kmean, y_train_kmean)

# Make predictions on the K-Means SMOTE train set
y_pred_train_kmean = xgb_classifier.predict(X_train_kmean)

# Make predictions on the K-Means SMOTE test set
y_pred_test_kmean = xgb_classifier.predict(X_test_kmean)

# Evaluate the performance of the classifier on K-Means SMOTE train and test sets
accuracy_train_kmean = accuracy_score(y_train_kmean, y_pred_train_kmean)
precision_train_kmean = precision_score(y_train_kmean, y_pred_train_kmean, average='weighted')
recall_train_kmean = recall_score(y_train_kmean, y_pred_train_kmean, average='weighted')
f1_score_train_kmean = f1_score(y_train_kmean, y_pred_train_kmean, average='weighted')

accuracy_test_kmean = accuracy_score(y_test_kmean, y_pred_test_kmean)
precision_test_kmean = precision_score(y_test_kmean, y_pred_test_kmean, average='weighted')
recall_test_kmean = recall_score(y_test_kmean, y_pred_test_kmean, average='weighted')
f1_score_test_kmean = f1_score(y_test_kmean, y_pred_test_kmean, average='weighted')

# Train the classifier on the Borderline SMOTE-resampled data
xgb_classifier.fit(X_train_border, y_train_border)

# Make predictions on the Borderline SMOTE train set
y_pred_train_border = xgb_classifier.predict(X_train_border)

# Make predictions on the Borderline SMOTE test set
y_pred_test_border = xgb_classifier.predict(X_test_border)

# Evaluate the performance of the classifier on Borderline SMOTE train and test sets
accuracy_train_border = accuracy_score(y_train_border, y_pred_train_border)
precision_train_border = precision_score(y_train_border, y_pred_train_border, average='weighted')
recall_train_border = recall_score(y_train_border, y_pred_train_border, average='weighted')
f1_score_train_border = f1_score(y_train_border, y_pred_train_border, average='weighted')

accuracy_test_border = accuracy_score(y_test_border, y_pred_test_border)
precision_test_border = precision_score(y_test_border, y_pred_test_border, average='weighted')
recall_test_border = recall_score(y_test_border, y_pred_test_border, average='weighted')
f1_score_test_border = f1_score(y_test_border, y_pred_test_border, average='weighted')

# Train the classifier on the ADASYN-resampled data
xgb_classifier.fit(X_train_ad, y_train_ad)

# Make predictions on the ADASYN train set
y_pred_train_ad = xgb_classifier.predict(X_train_ad)

# Make predictions on the ADASYN test set
y_pred_test_ad = xgb_classifier.predict(X_test_ad)

# Evaluate the performance of the classifier on ADASYN train and test sets
accuracy_train_ad = accuracy_score(y_train_ad, y_pred_train_ad)
precision_train_ad = precision_score(y_train_ad, y_pred_train_ad, average='weighted')
recall_train_ad = recall_score(y_train_ad, y_pred_train_ad, average='weighted')
f1_score_train_ad = f1_score(y_train_ad, y_pred_train_ad, average='weighted')

accuracy_test_ad = accuracy_score(y_test_ad, y_pred_test_ad)
precision_test_ad = precision_score(y_test_ad, y_pred_test_ad, average='weighted')
recall_test_ad = recall_score(y_test_ad, y_pred_test_ad, average='weighted')
f1_score_test_ad = f1_score(y_test_ad, y_pred_test_ad, average='weighted')

# Train the classifier on the original data
xgb_classifier.fit(X_train, y_train)

# Make predictions on the original train set
y_pred_train = xgb_classifier.predict(X_train)

# Make predictions on the original test set
y_pred_test = xgb_classifier.predict(X_test)

# Evaluate the performance of the classifier on the original train and test sets
accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, average='weighted')
recall_train = recall_score(y_train, y_pred_train, average='weighted')
f1_score_train = f1_score(y_train, y_pred_train, average='weighted')

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, average='weighted')
recall_test = recall_score(y_test, y_pred_test, average='weighted')
f1_score_test = f1_score(y_test, y_pred_test, average='weighted')

# Define the performance metrics and their corresponding values
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
results = [
    ["SMOTE (Train)", round(accuracy_train_smote, 4), round(precision_train_smote, 4), round(recall_train_smote, 4), round(f1_score_train_smote, 4)],
    ["SMOTE (Test)", round(accuracy_test_smote, 4), round(precision_test_smote, 4), round(recall_test_smote, 4), round(f1_score_test_smote, 4)],
    ["K-Means SMOTE (Train)", round(accuracy_train_kmean, 4), round(precision_train_kmean, 4), round(recall_train_kmean, 4), round(f1_score_train_kmean, 4)],
    ["K-Means SMOTE (Test)", round(accuracy_test_kmean, 4), round(precision_test_kmean, 4), round(recall_test_kmean, 4), round(f1_score_test_kmean, 4)],
    ["Borderline SMOTE (Train)", round(accuracy_train_border, 4), round(precision_train_border, 4), round(recall_train_border, 4), round(f1_score_train_border, 4)],
    ["Borderline SMOTE (Test)", round(accuracy_test_border, 4), round(precision_test_border, 4), round(recall_test_border, 4), round(f1_score_test_border, 4)],
    ["ADASYN (Train)", round(accuracy_train_ad, 4), round(precision_train_ad, 4), round(recall_train_ad, 4), round(f1_score_train_ad, 4)],
    ["ADASYN (Test)", round(accuracy_test_ad, 4), round(precision_test_ad, 4), round(recall_test_ad, 4), round(f1_score_test_ad, 4)],
    ["Without Oversampling (Train)", round(accuracy_train, 4), round(precision_train, 4), round(recall_train, 4), round(f1_score_train, 4)],
    ["Without Oversampling (Test)", round(accuracy_test, 4), round(precision_test, 4), round(recall_test, 4), round(f1_score_test, 4)]
]


# Print the results in table format
table = tabulate(results, headers=["XGBoost", "Accuracy", "Precision", "Recall", "F1 Score"], tablefmt="presto")
print(table)

#LightGBM

from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Create an AdaBoost classifier object
lgbm_classifier = LGBMClassifier(random_state=42)

# Train the classifier on the SMOTE-resampled data
lgbm_classifier.fit(X_train_smote, y_train_smote)

# Make predictions on the SMOTE train set
y_pred_train_smote = lgbm_classifier.predict(X_train_smote)

# Make predictions on the SMOTE test set
y_pred_test_smote = lgbm_classifier.predict(X_test_smote)

# Evaluate the performance of the classifier on SMOTE train and test sets
accuracy_train_smote = accuracy_score(y_train_smote, y_pred_train_smote)
precision_train_smote = precision_score(y_train_smote, y_pred_train_smote, average='weighted')
recall_train_smote = recall_score(y_train_smote, y_pred_train_smote, average='weighted')
f1_score_train_smote = f1_score(y_train_smote, y_pred_train_smote, average='weighted')

accuracy_test_smote = accuracy_score(y_test_smote, y_pred_test_smote)
precision_test_smote = precision_score(y_test_smote, y_pred_test_smote, average='weighted')
recall_test_smote = recall_score(y_test_smote, y_pred_test_smote, average='weighted')
f1_score_test_smote = f1_score(y_test_smote, y_pred_test_smote, average='weighted')

# Train the classifier on the K-Means SMOTE-resampled data
lgbm_classifier.fit(X_train_kmean, y_train_kmean)

# Make predictions on the K-Means SMOTE train set
y_pred_train_kmean = lgbm_classifier.predict(X_train_kmean)

# Make predictions on the K-Means SMOTE test set
y_pred_test_kmean = lgbm_classifier.predict(X_test_kmean)

# Evaluate the performance of the classifier on K-Means SMOTE train and test sets
accuracy_train_kmean = accuracy_score(y_train_kmean, y_pred_train_kmean)
precision_train_kmean = precision_score(y_train_kmean, y_pred_train_kmean, average='weighted')
recall_train_kmean = recall_score(y_train_kmean, y_pred_train_kmean, average='weighted')
f1_score_train_kmean = f1_score(y_train_kmean, y_pred_train_kmean, average='weighted')

accuracy_test_kmean = accuracy_score(y_test_kmean, y_pred_test_kmean)
precision_test_kmean = precision_score(y_test_kmean, y_pred_test_kmean, average='weighted')
recall_test_kmean = recall_score(y_test_kmean, y_pred_test_kmean, average='weighted')
f1_score_test_kmean = f1_score(y_test_kmean, y_pred_test_kmean, average='weighted')

# Train the classifier on the Borderline SMOTE-resampled data
lgbm_classifier.fit(X_train_border, y_train_border)

# Make predictions on the Borderline SMOTE train set
y_pred_train_border = lgbm_classifier.predict(X_train_border)

# Make predictions on the Borderline SMOTE test set
y_pred_test_border = lgbm_classifier.predict(X_test_border)

# Evaluate the performance of the classifier on Borderline SMOTE train and test sets
accuracy_train_border = accuracy_score(y_train_border, y_pred_train_border)
precision_train_border = precision_score(y_train_border, y_pred_train_border, average='weighted')
recall_train_border = recall_score(y_train_border, y_pred_train_border, average='weighted')
f1_score_train_border = f1_score(y_train_border, y_pred_train_border, average='weighted')

accuracy_test_border = accuracy_score(y_test_border, y_pred_test_border)
precision_test_border = precision_score(y_test_border, y_pred_test_border, average='weighted')
recall_test_border = recall_score(y_test_border, y_pred_test_border, average='weighted')
f1_score_test_border = f1_score(y_test_border, y_pred_test_border, average='weighted')

# Train the classifier on the ADASYN-resampled data
lgbm_classifier.fit(X_train_ad, y_train_ad)

# Make predictions on the ADASYN train set
y_pred_train_ad = lgbm_classifier.predict(X_train_ad)

# Make predictions on the ADASYN test set
y_pred_test_ad = lgbm_classifier.predict(X_test_ad)

# Evaluate the performance of the classifier on ADASYN train and test sets
accuracy_train_ad = accuracy_score(y_train_ad, y_pred_train_ad)
precision_train_ad = precision_score(y_train_ad, y_pred_train_ad, average='weighted')
recall_train_ad = recall_score(y_train_ad, y_pred_train_ad, average='weighted')
f1_score_train_ad = f1_score(y_train_ad, y_pred_train_ad, average='weighted')

accuracy_test_ad = accuracy_score(y_test_ad, y_pred_test_ad)
precision_test_ad = precision_score(y_test_ad, y_pred_test_ad, average='weighted')
recall_test_ad = recall_score(y_test_ad, y_pred_test_ad, average='weighted')
f1_score_test_ad = f1_score(y_test_ad, y_pred_test_ad, average='weighted')

# Train the classifier on the original data
lgbm_classifier.fit(X_train, y_train)

# Make predictions on the original train set
y_pred_train = lgbm_classifier.predict(X_train)

# Make predictions on the original test set
y_pred_test = lgbm_classifier.predict(X_test)

# Evaluate the performance of the classifier on the original train and test sets
accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, average='weighted')
recall_train = recall_score(y_train, y_pred_train, average='weighted')
f1_score_train = f1_score(y_train, y_pred_train, average='weighted')

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, average='weighted')
recall_test = recall_score(y_test, y_pred_test, average='weighted')
f1_score_test = f1_score(y_test, y_pred_test, average='weighted')

# Define the performance metrics and their corresponding values
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
results = [
    ["SMOTE (Train)", round(accuracy_train_smote, 4), round(precision_train_smote, 4), round(recall_train_smote, 4), round(f1_score_train_smote, 4)],
    ["SMOTE (Test)", round(accuracy_test_smote, 4), round(precision_test_smote, 4), round(recall_test_smote, 4), round(f1_score_test_smote, 4)],
    ["K-Means SMOTE (Train)", round(accuracy_train_kmean, 4), round(precision_train_kmean, 4), round(recall_train_kmean, 4), round(f1_score_train_kmean, 4)],
    ["K-Means SMOTE (Test)", round(accuracy_test_kmean, 4), round(precision_test_kmean, 4), round(recall_test_kmean, 4), round(f1_score_test_kmean, 4)],
    ["Borderline SMOTE (Train)", round(accuracy_train_border, 4), round(precision_train_border, 4), round(recall_train_border, 4), round(f1_score_train_border, 4)],
    ["Borderline SMOTE (Test)", round(accuracy_test_border, 4), round(precision_test_border, 4), round(recall_test_border, 4), round(f1_score_test_border, 4)],
    ["ADASYN (Train)", round(accuracy_train_ad, 4), round(precision_train_ad, 4), round(recall_train_ad, 4), round(f1_score_train_ad, 4)],
    ["ADASYN (Test)", round(accuracy_test_ad, 4), round(precision_test_ad, 4), round(recall_test_ad, 4), round(f1_score_test_ad, 4)],
    ["Without Oversampling (Train)", round(accuracy_train, 4), round(precision_train, 4), round(recall_train, 4), round(f1_score_train, 4)],
    ["Without Oversampling (Test)", round(accuracy_test, 4), round(precision_test, 4), round(recall_test, 4), round(f1_score_test, 4)]
]


# Print the results in table format
table = tabulate(results, headers=["LightGBM", "Accuracy", "Precision", "Recall", "F1 Score"], tablefmt="presto")
print(table)

#MLP

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

# Create an AdaBoost classifier object
mlp_classifier = MLPClassifier(random_state=42)

# Train the classifier on the SMOTE-resampled data
mlp_classifier.fit(X_train_smote, y_train_smote)

# Make predictions on the SMOTE train set
y_pred_train_smote = mlp_classifier.predict(X_train_smote)

# Make predictions on the SMOTE test set
y_pred_test_smote = mlp_classifier.predict(X_test_smote)

# Evaluate the performance of the classifier on SMOTE train and test sets
accuracy_train_smote = accuracy_score(y_train_smote, y_pred_train_smote)
precision_train_smote = precision_score(y_train_smote, y_pred_train_smote, average='weighted')
recall_train_smote = recall_score(y_train_smote, y_pred_train_smote, average='weighted')
f1_score_train_smote = f1_score(y_train_smote, y_pred_train_smote, average='weighted')

accuracy_test_smote = accuracy_score(y_test_smote, y_pred_test_smote)
precision_test_smote = precision_score(y_test_smote, y_pred_test_smote, average='weighted')
recall_test_smote = recall_score(y_test_smote, y_pred_test_smote, average='weighted')
f1_score_test_smote = f1_score(y_test_smote, y_pred_test_smote, average='weighted')

# Train the classifier on the K-Means SMOTE-resampled data
mlp_classifier.fit(X_train_kmean, y_train_kmean)

# Make predictions on the K-Means SMOTE train set
y_pred_train_kmean = mlp_classifier.predict(X_train_kmean)

# Make predictions on the K-Means SMOTE test set
y_pred_test_kmean = mlp_classifier.predict(X_test_kmean)

# Evaluate the performance of the classifier on K-Means SMOTE train and test sets
accuracy_train_kmean = accuracy_score(y_train_kmean, y_pred_train_kmean)
precision_train_kmean = precision_score(y_train_kmean, y_pred_train_kmean, average='weighted')
recall_train_kmean = recall_score(y_train_kmean, y_pred_train_kmean, average='weighted')
f1_score_train_kmean = f1_score(y_train_kmean, y_pred_train_kmean, average='weighted')

accuracy_test_kmean = accuracy_score(y_test_kmean, y_pred_test_kmean)
precision_test_kmean = precision_score(y_test_kmean, y_pred_test_kmean, average='weighted')
recall_test_kmean = recall_score(y_test_kmean, y_pred_test_kmean, average='weighted')
f1_score_test_kmean = f1_score(y_test_kmean, y_pred_test_kmean, average='weighted')

# Train the classifier on the Borderline SMOTE-resampled data
mlp_classifier.fit(X_train_border, y_train_border)

# Make predictions on the Borderline SMOTE train set
y_pred_train_border = mlp_classifier.predict(X_train_border)

# Make predictions on the Borderline SMOTE test set
y_pred_test_border = mlp_classifier.predict(X_test_border)

# Evaluate the performance of the classifier on Borderline SMOTE train and test sets
accuracy_train_border = accuracy_score(y_train_border, y_pred_train_border)
precision_train_border = precision_score(y_train_border, y_pred_train_border, average='weighted')
recall_train_border = recall_score(y_train_border, y_pred_train_border, average='weighted')
f1_score_train_border = f1_score(y_train_border, y_pred_train_border, average='weighted')

accuracy_test_border = accuracy_score(y_test_border, y_pred_test_border)
precision_test_border = precision_score(y_test_border, y_pred_test_border, average='weighted')
recall_test_border = recall_score(y_test_border, y_pred_test_border, average='weighted')
f1_score_test_border = f1_score(y_test_border, y_pred_test_border, average='weighted')

# Train the classifier on the ADASYN-resampled data
mlp_classifier.fit(X_train_ad, y_train_ad)

# Make predictions on the ADASYN train set
y_pred_train_ad = mlp_classifier.predict(X_train_ad)

# Make predictions on the ADASYN test set
y_pred_test_ad = mlp_classifier.predict(X_test_ad)

# Evaluate the performance of the classifier on ADASYN train and test sets
accuracy_train_ad = accuracy_score(y_train_ad, y_pred_train_ad)
precision_train_ad = precision_score(y_train_ad, y_pred_train_ad, average='weighted')
recall_train_ad = recall_score(y_train_ad, y_pred_train_ad, average='weighted')
f1_score_train_ad = f1_score(y_train_ad, y_pred_train_ad, average='weighted')

accuracy_test_ad = accuracy_score(y_test_ad, y_pred_test_ad)
precision_test_ad = precision_score(y_test_ad, y_pred_test_ad, average='weighted')
recall_test_ad = recall_score(y_test_ad, y_pred_test_ad, average='weighted')
f1_score_test_ad = f1_score(y_test_ad, y_pred_test_ad, average='weighted')

# Train the classifier on the original data
mlp_classifier.fit(X_train, y_train)

# Make predictions on the original train set
y_pred_train = mlp_classifier.predict(X_train)

# Make predictions on the original test set
y_pred_test = mlp_classifier.predict(X_test)

# Evaluate the performance of the classifier on the original train and test sets
accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, average='weighted')
recall_train = recall_score(y_train, y_pred_train, average='weighted')
f1_score_train = f1_score(y_train, y_pred_train, average='weighted')

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, average='weighted')
recall_test = recall_score(y_test, y_pred_test, average='weighted')
f1_score_test = f1_score(y_test, y_pred_test, average='weighted')

# Define the performance metrics and their corresponding values
metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
results = [
    ["SMOTE (Train)", round(accuracy_train_smote, 4), round(precision_train_smote, 4), round(recall_train_smote, 4), round(f1_score_train_smote, 4)],
    ["SMOTE (Test)", round(accuracy_test_smote, 4), round(precision_test_smote, 4), round(recall_test_smote, 4), round(f1_score_test_smote, 4)],
    ["K-Means SMOTE (Train)", round(accuracy_train_kmean, 4), round(precision_train_kmean, 4), round(recall_train_kmean, 4), round(f1_score_train_kmean, 4)],
    ["K-Means SMOTE (Test)", round(accuracy_test_kmean, 4), round(precision_test_kmean, 4), round(recall_test_kmean, 4), round(f1_score_test_kmean, 4)],
    ["Borderline SMOTE (Train)", round(accuracy_train_border, 4), round(precision_train_border, 4), round(recall_train_border, 4), round(f1_score_train_border, 4)],
    ["Borderline SMOTE (Test)", round(accuracy_test_border, 4), round(precision_test_border, 4), round(recall_test_border, 4), round(f1_score_test_border, 4)],
    ["ADASYN (Train)", round(accuracy_train_ad, 4), round(precision_train_ad, 4), round(recall_train_ad, 4), round(f1_score_train_ad, 4)],
    ["ADASYN (Test)", round(accuracy_test_ad, 4), round(precision_test_ad, 4), round(recall_test_ad, 4), round(f1_score_test_ad, 4)],
    ["Without Oversampling (Train)", round(accuracy_train, 4), round(precision_train, 4), round(recall_train, 4), round(f1_score_train, 4)],
    ["Without Oversampling (Test)", round(accuracy_test, 4), round(precision_test, 4), round(recall_test, 4), round(f1_score_test, 4)]
]


# Print the results in table format
table = tabulate(results, headers=["MLP", "Accuracy", "Precision", "Recall", "F1 Score"], tablefmt="presto")
print(table)

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from tabulate import tabulate

def ensemble(X_train, y_train, X_test, y_test):
    # Create a Random Forest classifier object
    rf_classifier = RandomForestClassifier(random_state=42)

    # Train the Random Forest classifier on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data using Random Forest
    rf_predictions = rf_classifier.predict(X_test)

    # Create an MLP classifier object
    mlp_classifier = XGBClassifier(random_state=42)

    # Train the MLP classifier on the training data
    mlp_classifier.fit(X_train, y_train)

    # Make predictions on the test data using MLP
    mlp_predictions = mlp_classifier.predict(X_test)

    # Create an ensemble by combining the predictions
    ensemble_predictions = np.array([rf_predictions, mlp_predictions])
    # Take the majority vote by selecting the most common prediction for each sample
    ensemble_predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x.astype(int))), axis=0, arr=ensemble_predictions)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='weighted')
    recall = recall_score(y_test, ensemble_predictions, average='weighted')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='weighted')

    return ensemble_accuracy, precision, recall, f1_score_a


# Calculate ensemble results for different datasets
results = []
results.append(["Original Data"] + list(ensemble(X_train, y_train, X_test, y_test)))
results.append(["SMOTE"] + list(ensemble(X_train_smote, y_train_smote, X_test_smote, y_test_smote)))
results.append(["K-Means SMOTE"] + list(ensemble(X_train_kmean, y_train_kmean, X_test_kmean, y_test_kmean)))
results.append(["Borderline SMOTE"] + list(ensemble(X_train_border, y_train_border, X_test_border, y_test_border)))
results.append(["ADASYN"] + list(ensemble(X_train_ad, y_train_ad, X_test_ad, y_test_ad)))

# Print the results in table format
headers = ["Dataset", "Ensemble Accuracy", "Precision", "Recall", "F1 Score"]
table = tabulate(results, headers=headers, tablefmt="presto")
print(table)

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from tabulate import tabulate

def ensemble(X_train, y_train, X_test, y_test):
    # Create a Random Forest classifier object
    rf_classifier = RandomForestClassifier(random_state=42)

    # Train the Random Forest classifier on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data using Random Forest
    rf_predictions = rf_classifier.predict(X_test)

    # Create an MLP classifier object
    mlp_classifier = LGBMClassifier(random_state=42)

    # Train the MLP classifier on the training data
    mlp_classifier.fit(X_train, y_train)

    # Make predictions on the test data using MLP
    mlp_predictions = mlp_classifier.predict(X_test)

    # Create an ensemble by combining the predictions
    ensemble_predictions = np.array([rf_predictions, mlp_predictions])
    # Take the majority vote by selecting the most common prediction for each sample
    ensemble_predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x.astype(int))), axis=0, arr=ensemble_predictions)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='weighted')
    recall = recall_score(y_test, ensemble_predictions, average='weighted')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='weighted')

    return ensemble_accuracy, precision, recall, f1_score_a


# Calculate ensemble results for different datasets
results = []
results.append(["Original Data"] + list(ensemble(X_train, y_train, X_test, y_test)))
results.append(["SMOTE"] + list(ensemble(X_train_smote, y_train_smote, X_test_smote, y_test_smote)))
results.append(["K-Means SMOTE"] + list(ensemble(X_train_kmean, y_train_kmean, X_test_kmean, y_test_kmean)))
results.append(["Borderline SMOTE"] + list(ensemble(X_train_border, y_train_border, X_test_border, y_test_border)))
results.append(["ADASYN"] + list(ensemble(X_train_ad, y_train_ad, X_test_ad, y_test_ad)))

# Print the results in table format
headers = ["Dataset", "Ensemble Accuracy", "Precision", "Recall", "F1 Score"]
table = tabulate(results, headers=headers, tablefmt="presto")
print(table)

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from tabulate import tabulate

def ensemble(X_train, y_train, X_test, y_test):
    # Create a Random Forest classifier object
    rf_classifier = RandomForestClassifier(random_state=42)

    # Train the Random Forest classifier on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data using Random Forest
    rf_predictions = rf_classifier.predict(X_test)

    # Create an MLP classifier object
    mlp_classifier = CatBoostClassifier(random_state=42)

    # Train the MLP classifier on the training data
    mlp_classifier.fit(X_train, y_train)

    # Make predictions on the test data using MLP
    mlp_predictions = mlp_classifier.predict(X_test)

    # Create an ensemble by combining the predictions
    ensemble_predictions = np.array([rf_predictions, mlp_predictions])
    # Take the majority vote by selecting the most common prediction for each sample
    ensemble_predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x.astype(int))), axis=0, arr=ensemble_predictions)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='weighted')
    recall = recall_score(y_test, ensemble_predictions, average='weighted')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='weighted')

    return ensemble_accuracy, precision, recall, f1_score_a


# Calculate ensemble results for different datasets
results = []
results.append(["Original Data"] + list(ensemble(X_train, y_train, X_test, y_test)))
results.append(["SMOTE"] + list(ensemble(X_train_smote, y_train_smote, X_test_smote, y_test_smote)))
results.append(["K-Means SMOTE"] + list(ensemble(X_train_kmean, y_train_kmean, X_test_kmean, y_test_kmean)))
results.append(["Borderline SMOTE"] + list(ensemble(X_train_border, y_train_border, X_test_border, y_test_border)))
results.append(["ADASYN"] + list(ensemble(X_train_ad, y_train_ad, X_test_ad, y_test_ad)))

# Print the results in table format
headers = ["Dataset", "Ensemble Accuracy", "Precision", "Recall", "F1 Score"]
table = tabulate(results, headers=headers, tablefmt="presto")
print(table)

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from tabulate import tabulate

def ensemble(X_train, y_train, X_test, y_test):
    # Create a Random Forest classifier object
    rf_classifier = RandomForestClassifier(random_state=42)

    # Train the Random Forest classifier on the training data
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test data using Random Forest
    rf_predictions = rf_classifier.predict(X_test)

    # Create an MLP classifier object
    mlp_classifier = AdaBoostClassifier(random_state=42)

    # Train the MLP classifier on the training data
    mlp_classifier.fit(X_train, y_train)

    # Make predictions on the test data using MLP
    mlp_predictions = mlp_classifier.predict(X_test)

    # Create an ensemble by combining the predictions
    ensemble_predictions = np.array([rf_predictions, mlp_predictions])
    # Take the majority vote by selecting the most common prediction for each sample
    ensemble_predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x.astype(int))), axis=0, arr=ensemble_predictions)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='weighted')
    recall = recall_score(y_test, ensemble_predictions, average='weighted')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='weighted')

    return ensemble_accuracy, precision, recall, f1_score_a


# Calculate ensemble results for different datasets
results = []
results.append(["Original Data"] + list(ensemble(X_train, y_train, X_test, y_test)))
results.append(["SMOTE"] + list(ensemble(X_train_smote, y_train_smote, X_test_smote, y_test_smote)))
results.append(["K-Means SMOTE"] + list(ensemble(X_train_kmean, y_train_kmean, X_test_kmean, y_test_kmean)))
results.append(["Borderline SMOTE"] + list(ensemble(X_train_border, y_train_border, X_test_border, y_test_border)))
results.append(["ADASYN"] + list(ensemble(X_train_ad, y_train_ad, X_test_ad, y_test_ad)))

# Print the results in table format
headers = ["Dataset", "Ensemble Accuracy", "Precision", "Recall", "F1 Score"]
table = tabulate(results, headers=headers, tablefmt="presto")
print(table)

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from tabulate import tabulate

def ensemble(X_train, y_train, X_test, y_test, classifiers):
    predictions = []

    # Train the classifiers individually
    for clf in classifiers:
        clf.fit(X_train, y_train)

    # Perform predictions with each classifier
    predictions = []
    for clf in classifiers:
        clf_predictions = clf.predict(X_test)
        predictions.append(clf_predictions)

    # Dynamic ensemble
    ensemble_predictions = []
    for i in range(len(X_test)):
        votes = {}  # Dictionary to store the votes for each class label
        for clf_index, clf in enumerate(classifiers):
            clf_prediction = predictions[clf_index][i]
            if isinstance(clf_prediction, np.int64) or isinstance(clf_prediction, np.float64):
                clf_prediction = [clf_prediction]  # Convert numpy.int64 or numpy.float64 to list
            clf_prediction_tuple = tuple(clf_prediction)
            if clf_prediction_tuple in votes:
                votes[clf_prediction_tuple] += 1
            else:
                votes[clf_prediction_tuple] = 1

        # Select the class label with the maximum votes
        ensemble_prediction = max(votes, key=votes.get)
        ensemble_predictions.append(ensemble_prediction)

    # Evaluate the performance of the ensemble model
    ensemble_accuracy = accuracy_score(y_test, ensemble_predictions)
    precision = precision_score(y_test, ensemble_predictions, average='macro')
    recall = recall_score(y_test, ensemble_predictions, average='macro')
    f1_score_a = f1_score(y_test, ensemble_predictions, average='macro')

    return ensemble_accuracy, precision, recall, f1_score_a




# Define the classifiers for ensembling
classifiers = [
    RandomForestClassifier(n_estimators=80, max_depth=20, random_state=42),
    XGBClassifier(n_estimators=50, max_depth=20, random_state=42),
    CatBoostClassifier(n_estimators=50, max_depth=15, random_state=42, verbose=False),
    LGBMClassifier(n_estimators=50, max_depth=20, random_state=42),
    AdaBoostClassifier(n_estimators=80, learning_rate=0.5, random_state=42),
]

# Calculate ensemble results for different datasets
results = []
results.append(["Original Data"] + list(ensemble(X_train, y_train, X_test, y_test, classifiers)))
results.append(["SMOTE"] + list(ensemble(X_train_smote, y_train_smote, X_test_smote, y_test_smote, classifiers)))
results.append(["K-Means SMOTE"] + list(ensemble(X_train_kmean, y_train_kmean, X_test_kmean, y_test_kmean, classifiers)))
results.append(["Borderline SMOTE"] + list(ensemble(X_train_border, y_train_border, X_test_border, y_test_border, classifiers)))
results.append(["ADASYN"] + list(ensemble(X_train_ad, y_train_ad, X_test_ad, y_test_ad, classifiers)))

# Print the results in table format
headers = ["Ensemble", "Ensemble Accuracy", "Precision", "Recall", "F1 Score"]
table = tabulate(results, headers=headers, tablefmt="presto")
print(table)

