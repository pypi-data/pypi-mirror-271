# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 13:41:26 2021

When the outcome is imbalanced, the standard cutoff 0.5 may not correct. 
When we still want to use standard ML models, we can tune the cutoff for classification to 
achieve better performance. The cutoff has to be tunned using the traning data. Then being
applied to test set.

@author: yipeng.song@hotmail.com
"""
# %% load into required packages
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn import model_selection
from dummyML.evaluate_models.classification_metrics import predict_test_set_

# when necessary, suppress the warnings, mainly for testing
from warnings import simplefilter
from sklearn.exceptions import ConvergenceWarning

# %% binary classification: test set evaluation
def classification_evaluation_test_imb(
	results, 
	X_train, y_train, 
	X_test, y_test, 
	given_metric=metrics.balanced_accuracy_score):
    """evaluate the selected models' performance on the test set

    Args:
        results (dict): key, model name; value, saved models and model selection.
        X_train (np.ndarray): train set X
        y_train (np.ndarray): train set y
        X_test (np.ndarray): test set X
        y_test (np.ndarray): test set y
        given_metric (function, optional): the given metric to evaluate the model. Defaults to metrics.balanced_accuracy_score.

    Returns:
        pd.dataframe: multiple performance metrics for all the saved models.
    """
    # extract the keys in the dict of the results
    model_names = list(results.keys())

    # get the metrics on the test set for all the selected models
    models_metrics_test = {}
    for key in model_names:
        selected_model = results[key].selected_model_

        # get the probabilistic prediction for y_train and y_test
        _, _, _, y_train_prob = predict_test_set_(selected_model, X_train, y_train)
        _, _, _, y_test_prob = predict_test_set_(selected_model, X_test, y_test)    

        # get the labels
        labels = selected_model.classes_

        # get the metrics on the test set
        models_metrics_test[key] = binary_evaluation_base_imb_(
            y_train, y_train_prob, 
            y_test, y_test_prob, 
            labels, 
            given_metric=given_metric)

    # generate the model evaluation metrics
    models_metrics_test = pd.DataFrame(models_metrics_test)
    models_metrics_test.index = [ele + "_test" for ele in models_metrics_test.index]
    return models_metrics_test

# %% classification evaluation for a single model
def binary_evaluation_base_imb_(
	y_train, y_train_prob, 
    y_test, y_test_prob, 
    labels, given_metric=metrics.balanced_accuracy_score):
    
    # get the optimal cutoff based on the training errors
    cutoffs = np.linspace(y_train_prob.min(), y_train_prob.max(), 1000)
    train_scores = get_train_scores(
        y_train,
        y_train_prob,
        cutoffs,
        labels,
        given_metric=given_metric,
    )
    max_value = np.max(train_scores)
    max_cutoffs = cutoffs[train_scores == max_value]
    mean_cutoff = 0.5 * (max_cutoffs.min() + max_cutoffs.max())

    # discretize the prob to get the predicted labels for y_test_prob
    y_test_hat = prob_discretize(y_test, y_test_prob, labels, cutoff=mean_cutoff)
    
    # get the metrics on the test set using y_test_hat
    custom_errors = eval_metrics(y_test, y_test_hat, labels)

    return custom_errors

# %% KFold CV error
def classification_evaluation_cv_imb(
    results,
    X,
    y,
    cv=10,
    given_metric=metrics.balanced_accuracy_score,
    n_jobs=10,
):
    """evaluate the selected models' performance using K-Fold CV and customized cutoff

    Args:
        results (dict): key, model name; value, saved models and model selection.
        X (np.ndarray): X
        y (np.ndarray): y
        cv (int, optional): K-Fold CV. Defaults to 10.
        given_metric (function, optional): used to tune the custom cutoff.
        n_jobs (int, optional): number of cores to be used. Defaults to 10.

    Returns:
        pd.dataframe: multiple performance metrics for all the saved models.
    """
    # extract the keys in the dict of the results
    model_names = list(results.keys())

    # get the metrics on all the data using K-Fold CV for the models
    models_metrics_cv = {}
    for key in model_names:
        selected_model = results[key].selected_model_
        models_metrics_cv[key] = binary_evaluation_cv_imb_(
            selected_model,
            X=X,
            y=y,
            cv=cv,
            given_metric=given_metric,
            n_jobs=n_jobs,
        )
    models_metrics_cv = pd.DataFrame(models_metrics_cv)

    return models_metrics_cv

# define a function to return the cross validated predictions
def get_y_prob_cv(selected_model, X, y, cv, n_jobs):
    y_hat_prob = None

    # probability estimation
    if hasattr(selected_model, "predict_proba"):
        y_hat_prob = model_selection.cross_val_predict(
            selected_model, X, y, cv=cv, n_jobs=n_jobs, method="predict_proba"
        )[:, 1]

    # non probability estimation for svm model
    if (not hasattr(selected_model, "predict_proba")) and hasattr(selected_model, "decision_function"):
        y_hat_prob = model_selection.cross_val_predict(
            selected_model, X, y, cv=cv, n_jobs=n_jobs, method="decision_function"
        )

    return y_hat_prob

def binary_evaluation_cv_imb_(selected_model, X, y, cv, given_metric, n_jobs=10):
    # get cv split for generating reproduiable results
    skcv = model_selection.StratifiedKFold(n_splits=cv, shuffle=True)

    # get the labels
    labels = selected_model.classes_

    # y_prob K-Fold CV
    y_hat_prob = get_y_prob_cv(selected_model, X, y, cv=skcv, n_jobs=n_jobs)

    # go through all the training and test sets during K-Fold CV
    metrics_cv = {}
    kth_cv = 0
    for train_index, test_index in skcv.split(X, y):
        y_train, y_test = y[train_index], y[test_index]
        y_train_prob, y_test_prob = y_hat_prob[train_index], y_hat_prob[test_index]
        metrics_cv[kth_cv] = binary_evaluation_base_imb_(y_train, y_train_prob, y_test, y_test_prob, labels, given_metric)
        kth_cv += 1

    return pd.DataFrame(metrics_cv).mean(axis=1)


# %% utility functions
# get the training scores for different cutoffs
def get_train_scores(y_train, y_train_prob, cutoffs, labels, given_metric):
    # go through all the cutoffs
    metrics_cutoffs = np.zeros(len(cutoffs))
    for i, cutoff in enumerate(cutoffs):
        y_train_pred = prob_discretize(y_train, y_train_prob, labels, cutoff=cutoff)
        metrics_cutoffs[i] = given_metric(y_train, y_train_pred)

    return metrics_cutoffs

# define a function to discretize the probability outputs to binary predictions
def prob_discretize(y, y_prob, labels, cutoff=0.5):
    """Dichotomize continuous probabilities to binary predictions

    Args:
        y (np.ndarray): outcome label
        y_prob (np.ndarray): the probability predictions of a machine learning model
        labels (list): the list contains the binary labels, [negative case, positive case]
        cutoff (float, optional): [description]. Defaults to 0.5.

    Returns:
        np.ndarray: the binary labels transformed from probability
    """
    y_pred = np.empty_like(y)
    y_pred.fill(labels[0])

    # discretize prob to binary labels
    y_pred[y_prob > cutoff] = labels[1]
    return y_pred

# define a function to calculate the different metrics
def eval_metrics(y_true, y_hat, labels):
    # confusion matrix
    CM = metrics.confusion_matrix(y_true, y_hat, labels=labels)
    TN = CM[0][0]
    FN = CM[1][0]
    TP = CM[1][1]
    FP = CM[0][1]

    # multiple evaluation metrics
    sensitivity = TP / (TP + FN)
    specificity = TN / (TN + FP)
    balanced_accuracy = (TP / (TP + FN) + TN / (TN + FP)) / 2
    recall = sensitivity
    precision = TP / (TP + FP)
    f1_score = 2 * TP / (2 * TP + FP + FN)

    # add negative and positive predictive value
    pos_pred_value = TP / (TP + FP)
    neg_pred_value = TN / (TN + FN)

    # metrics
    model_metrics = pd.Series(
        [
            sensitivity,
            specificity,
            balanced_accuracy,
            pos_pred_value,
            neg_pred_value,
            recall,
            precision,
            f1_score,
        ],
        index=[
            "sensitivity",
            "specificity",
            "balanced_accuracy",
            "positive_predictive_value",
            "negative_predictive_value",
            "recall",
            "precision",
            "f1_score",
        ],
    )

    return model_metrics

