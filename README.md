# SMOTE and Classification Models with Dynamic Ensemble

This repository contains a comprehensive study on handling class imbalance using various Synthetic Minority Over-sampling Techniques (SMOTE) and different classification models. Additionally, it includes the implementation of a Dynamic Ensemble approach to further improve the performance of the models. The dataset used in this study is related to landslide prediction and consists of various environmental features.

## Table of Contents
1. [Introduction](#introduction)
2. [Datasets](#datasets)
3. [Methods](#methods)
4. [Models](#models)
5. [Dynamic Ensemble](#dynamic-ensemble)
6. [Evaluation Metrics](#evaluation-metrics)
7. [Results](#results)
8. [Installation](#installation)
9. [Usage](#usage)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction
Class imbalance is a common issue in machine learning, especially in real-world datasets. This repository explores different SMOTE techniques to handle imbalanced data and evaluates their performance using various classification models. Additionally, a Dynamic Ensemble approach is implemented to combine the strengths of multiple models for better performance.

## Datasets
The dataset used in this study is related to landslide prediction and includes features like Temperature, Humidity, Pressure, Rain, Light, Accelerometer readings (Ax, Ay, Az), Gyroscope readings (Wx, Wy, Wz), Soil Moisture, and Movements. The target variable is the occurrence of a landslide.

## Methods
We have used the following oversampling techniques to handle class imbalance:
- SMOTE (Synthetic Minority Over-sampling Technique)
- KMeansSMOTE
- SVMSMOTE
- BorderlineSMOTE
- ADASYN

## Models
The following classification models were used to evaluate the performance of the oversampling techniques:
- RandomForestClassifier
- AdaBoostClassifier
- XGBClassifier
- LGBMClassifier
- CatBoostClassifier
- MLPClassifier (Multi-Layer Perceptron)

## Dynamic Ensemble
The Dynamic Ensemble approach combines predictions from multiple models based on their performance. This method dynamically selects the best models during the prediction phase to improve overall accuracy and robustness. The ensemble includes:
- Voting based on model performance
- Weighted averaging of predictions

## Evaluation Metrics
The performance of the models was evaluated using the following metrics:
- Accuracy
- Precision
- Recall
- F1 Score

## Results
The results of the study are summarized in tabular format, showing the performance metrics for each model and oversampling technique on both training and test datasets. The impact of the Dynamic Ensemble approach on the overall performance is also presented.

## Installation
To run the code in this repository, you need to have Python installed along with the required libraries. You can install the necessary packages using pip:
```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository:
```bash
git clone https://github.com/bluecodeindia/SMOTE-and-Classification-Models.git
```
2. Navigate to the repository directory:
```bash
cd SMOTE-and-Classification-Models
```
3. Run the Jupyter notebook or Python scripts to reproduce the results.

## Contributing
Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to customize this README file further according to your needs!