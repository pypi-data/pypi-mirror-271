# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 17:42:38 2021

This file define the tests for testing utilities

@author: yipeng.song@hotmail.com
"""
import os
import unittest
from dummyML.automate_analysis import automate_analysis

# %% some default parameters used in the automate data analysis
## the the column of the ID in the data
index_col = 0

## arguments to control the preprocessing steps
cat_levels_threshold = 15
missing_threshold = 0.5

## log information & save the model
verbose = 0
save_results = False

## arguments to control the training and test sets splitting
test_size = 0.2
random_state = 123

## arguments to control the selection and fitting of ML models
scaler = "standard"
decomposer = None
n_components = None
models = ["linear", "lasso", "ridge", "elasticNet", "svm", "gb", "rf"]
n_trials = 30
n_jobs = 10
max_iter = 100

## arguments to control the model evaluations
cv = 10
cv_force = False
eval_cv = False

#%% define the class to do testing
class TestAutomateDataAnalysis(unittest.TestCase):
    def test_regression(self):
        path2data = os.path.join(os.path.dirname(__file__), "../data/titanic.csv")
        outcome = "Age"
        output = automate_analysis(
            path2data,
            outcome,
            index_col=index_col,
            test_size=test_size,
            eval_cv=eval_cv,
            models=models,
            cv=cv,
            n_trials=n_trials,
            n_jobs=n_jobs,
            verbose=verbose,
            save_results=save_results,
            random_state=random_state,
        )
        pass_test = True if output is None else False
        print(pass_test)
        self.assertEqual(pass_test, True, "Regression tests failed.")

    def test_classification(self):
        path2data = os.path.join(os.path.dirname(__file__), "../data/titanic.csv")
        outcome = "Survived"
        output = automate_analysis(
            path2data,
            outcome,
            index_col=index_col,
            test_size=test_size,
            eval_cv=eval_cv,
            models=models,
            cv=cv,
            n_trials=n_trials,
            n_jobs=n_jobs,
            verbose=verbose,
            save_results=save_results,
            random_state=random_state,
        )
        pass_test = True if output is None else False
        print(pass_test)
        self.assertEqual(pass_test, True, "Classification tests failed.")

    def test_imb_classification(self):
        path2data = os.path.join(os.path.dirname(__file__), "../data/titanic.csv")
        outcome = "Survived"
        output = automate_analysis(
            path2data,
            outcome,
            imbalance_force=True,
            index_col=index_col,
            test_size=test_size,
            eval_cv=eval_cv,
            models=models,
            cv=cv,
            n_trials=n_trials,
            n_jobs=n_jobs,
            verbose=verbose,
            save_results=save_results,
            random_state=random_state,
        )
        pass_test = True if output is None else False
        print(pass_test)
        self.assertEqual(pass_test, True, "Imbalanced classification tests failed.")

    def test_multiclass_classification(self):
        path2data = os.path.join(os.path.dirname(__file__), "../data/iris.csv")
        outcome = "Species"
        output = automate_analysis(
            path2data,
            outcome,
            index_col=index_col,
            test_size=test_size,
            eval_cv=eval_cv,
            models=models,
            cv=cv,
            n_trials=n_trials,
            n_jobs=n_jobs,
            verbose=verbose,
            save_results=save_results,
            random_state=random_state,
        )
        pass_test = True if output is None else False
        print(pass_test)
        self.assertEqual(pass_test, True, "Multiclass classification tests failed.")


if __name__ == "__main__":
    unittest.main()
