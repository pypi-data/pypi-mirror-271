# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 17:42:38 2021

This file define the tests for testing utilities

@author: yipeng.song@hotmail.com
"""
import os
import unittest
from dummyML import preprocessing
from dummyML import utilities

# read into the data
path2data = os.path.join(os.path.dirname(__file__), "../data/titanic.csv")
data = utilities.read_data(path2data, index_col=0)
outcome = "Survived"
name = os.path.basename(path2data).split(".")[0] + "_" + outcome
X, y, _, _, saved_preprocess_steps = preprocessing.data_preprocessing(
    data,
    outcome,
    name,
    cat_levels_threshold=15,
    missing_threshold=0.5,
    for_future_test=True,
    verbose=0,
    save_results=False,
)

# test if preprocessing steps can be successfully be done
class TestPreprocessing(unittest.TestCase):
    def test_preprocess(self):
        """test if preprocessing procedure can be used"""
        pass_test = True
        if X.shape[0] != len(y):
            pass_test = False
        if len(y) == 0:
            pass_test = True

        self.assertEqual(pass_test, True, "Preprocessed data is not correct.")

    def test_future_preprocess(self):
        """test if the saved preprocessed procedure can be applied to raw data"""
        X_test = saved_preprocess_steps.transform(data)

        self.assertEqual(X_test.shape[1], X.shape[1])


if __name__ == "__main__":
    unittest.main()
