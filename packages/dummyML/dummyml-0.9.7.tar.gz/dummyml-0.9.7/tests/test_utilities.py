# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 17:42:38 2021

This file define the tests for testing utilities

@author: yipeng.song@hotmail.com
"""
import os
import numpy as np
import unittest
from dummyML import utilities

# get the path to the titanic data
path2data = os.path.join(os.path.dirname(__file__), "../data/titanic.csv")
data = utilities.read_data(path2data, index_col=0)


class TestUtilities(unittest.TestCase):
    def test_read_data(self):
        """test if read_data function in utilities can correctly load the data"""
        data_shape = data.shape
        self.assertEqual(
            data_shape, (891, 11), "csv file can not be loaded into Python"
        )

    def test_infer_task_string_multiclass(self):
        y = np.array(["1", "2", "3"], dtype="object")
        inferred_task = utilities.infer_task(y)
        self.assertEqual(inferred_task, "multi_clf")

    def test_infer_task_string_binary(self):
        y = np.array(["1", "2", "1", "2", "1"], dtype="object")
        inferred_task = utilities.infer_task(y)
        self.assertEqual(inferred_task, "binary_clf")

    def test_infer_task_reg(self):
        y = np.random.randn(15)
        inferred_task = utilities.infer_task(y)
        self.assertEqual(inferred_task, "reg")

    def test_infer_task_num_multiclass(self):
        y = np.array([1, 2, 3, 1, 2, 3, 2, 3, 4])
        inferred_task = utilities.infer_task(y)
        self.assertEqual(inferred_task, "multi_clf")


if __name__ == "__main__":
    unittest.main()
