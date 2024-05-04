# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:45:41 2021

This files include functions to do automatic data preprocessing

@author: yipeng.song@hotmail.com
"""
import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from dummyML import utilities

# %% a fun to do data preprocessing
def data_preprocessing(
    data,
    outcome,
    name,
    cat_levels_threshold=15,
    text_levels_threshold=15,
    missing_threshold=0.5,
    strategy="median",
    dummy_coding=True,
    for_future_test=False,
    verbose=1,
    save_results=True,
    root_path=None,
):
    """A simple automate data preprocessing step

    Args:
        data (pd.dataframe): Contains both the design matrix and outcome.
        outcome (str): the name of the outcome.
        name (str): The name of the data set for saving the data.
        cat_levels_threshold (int, optional): When the unique values of
            a column is less than this value, will take it as a categorical
            variable. Defaults to 15.
        text_levels_threshold (int, optional): When the unique values of
            a column is larger than this value and the elements are strings,
            will take it as a text variable and remove it. Defaults to 15.
        missing_threshold (float, optional): [0, 1], When the propotation
            of missing values larger than this value, remove the corresponding
            rows and columns. Defaults to 0.5.
        strategy (string, optional): What is the strategy to tackle missing values.
            Defaults to "median". Another option is "mean".
        dummy_coding (bool, optional): Whether to use dummy coding for categorical
            variables? Defaults to True. If False, ordinal encoder, coding categorical
            variables as integers, will be used. For tree based model, ordinal encoder
            is also a popular option, while for linear models, ordinal encoder is not a good idea.
        for_future_test (bool, optional): If the saved preprocessing is going
            to be used to preprocess the future test data, it is better set it
            as True. This argument is mainly about how to do one-hot encoding.
            When it is True, the first level will not be dropped and unknown class
            in the test set will be ignored. Default False.
        verbose (int, optional): whether to show log information.
            Defaults to 1. 1: show information; 0: not show information.
        save_results (bool, optional): whether to save the parameters, which
            will be useful to preprocess new data sets. Defaults to True.
        root_path (str, optional): the parent folder to save results.

    Raises:
        NameError: The outcome is not found in the data.

    Returns:
        X (np.ndarray): Design matrix.
        y (np.ndarray): outcome.
        feature_names (list of str): The names of the feature variables.
        sample_index (list of str): The row index of X and y in original data.
        saved_preprocess_steps (an object of self defined class): the saved
            preprocess steps for the preprocessing of future test set.
    """
    if outcome not in data.columns:
        raise NameError("the outcome is not found in the data")

    # rm the subjects with NAs in the y
    NAs = ["NA", "Null", "NULL", "NAN", "na", "NaN", "nan"]
    y_raw = data.loc[:, outcome]
    na_idx = [ele in NAs for ele in y_raw]
    if np.array(na_idx).sum() > 0:
        y_raw[na_idx] = np.nan
    kept_idx = np.logical_not(pd.isnull(y_raw))
    data = data.loc[kept_idx, :]

    # split data into X and y
    y_raw = data.loc[:, outcome]
    X_raw = data.drop(outcome, axis=1)

    # change all the integer features with less than cat_levels_threshould unique
    # values to be categorical
    unique_values = X_raw.apply(lambda x: len(pd.value_counts(x)), axis=0)
    category_cols = unique_values < cat_levels_threshold
    X_raw.loc[:, category_cols] = X_raw.loc[:, category_cols].astype(str)

    # rm cols contains text data, the cols with type object
    # and unique_values >= 15
    if cat_levels_threshold > text_levels_threshold:
        text_levels_threshold = cat_levels_threshold
    potential_text_cols = unique_values >= text_levels_threshold
    text_cols = np.logical_and(X_raw.dtypes == "object", potential_text_cols)
    text_cols_names = X_raw.columns[text_cols].to_list()
    if len(text_cols_names) > 0:
        if verbose == 1:
            print("An example of the dropped text data is: ")
            print(data.sample(5).loc[:, text_cols_names])
        X_raw.drop(text_cols_names, axis=1, inplace=True)

    # change the missing values in categorical variables as a new level
    # and set the column with object type to string to avoid mixed type problems
    data_cat_variables = X_raw.columns[X_raw.dtypes == "object"]
    data_cat = X_raw.loc[:, data_cat_variables].astype(str)
    data_cat.fillna("nan", inplace=True)
    X_raw.loc[:, data_cat_variables] = data_cat

    # set the infinite elements as nan
    X_raw.replace([np.inf, -np.inf], np.nan, inplace=True)

    # rm the cols and rows with a lot NAs
    data_NAs = pd.isnull(X_raw)
    col_idx = data_NAs.sum(axis=0) < missing_threshold * X_raw.shape[0]
    row_idx = data_NAs.sum(axis=1) < missing_threshold * X_raw.shape[1]
    X_raw = X_raw.loc[row_idx, col_idx]
    if verbose == 1:
        print(
            "{} rows and {} cols are removed due to NAs".format(
                (1 - row_idx).sum(), (1 - col_idx).sum()
            )
        )

    # remove all the rows with NAs in y
    y = y_raw.loc[X_raw.index]
    X = X_raw

    # remove all the rows contains NAs in y
    NonNA_idx = np.logical_not(pd.isnull(y))
    X = X.loc[NonNA_idx, :]
    y = y.loc[NonNA_idx]

    # rm colum with only a single unique value
    unique_values = X.apply(lambda x: len(pd.value_counts(x)), axis=0)
    X = X.loc[:, unique_values > 1]

    ## encoding the categorical variables
    # split numerical X and categorical X
    kept_variables = X.columns
    var_dtypes = X.dtypes
    cat_variables = kept_variables[var_dtypes == "object"]
    num_variables = kept_variables[var_dtypes != "object"]
    X_cat = X.loc[:, cat_variables]
    X_num = X.loc[:, num_variables]

    # encoding categorical variables and record the transformers
    if dummy_coding:
        if for_future_test:
            cat_encoder = OneHotEncoder(
                drop=None, sparse=False, handle_unknown="ignore"
            )
        else:
            cat_encoder = OneHotEncoder(
                drop="first", sparse=False, handle_unknown="error"
            )
        cat_encoder.fit(X_cat)
        X_cat_dummy = pd.DataFrame(
            data=cat_encoder.transform(X_cat),
            index=X_cat.index,
            columns=cat_encoder.get_feature_names_out(cat_variables),
        )
    else:
        cat_encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value", unknown_value=np.nan
        )
        cat_encoder.fit(X_cat)
        X_cat_dummy = pd.DataFrame(
            data=cat_encoder.transform(X_cat),
            index=X_cat.index,
            columns=X_cat.columns,
        )
    # recombine the cat and num data sets
    X = pd.concat([X_num, X_cat_dummy], axis=1)
    feature_names = X.columns
    sample_index = X.index.to_list()

    # input missing values
    imputer = SimpleImputer(strategy=strategy)
    imputer.fit(X)
    X = imputer.transform(X)

    # transform y to np array
    if type(y) == pd.core.series.Series:
        y = y.to_numpy()

    # check the document of np.savez_compressed to see how to load the saved data
    if save_results:
        # target_path
        if root_path is None:
            target_path = os.path.join("./results", name)
        else:
            target_path = os.path.join(root_path, name)
        if not os.path.isdir(target_path):
            os.mkdir(target_path)

        # path to the preprocessed data
        path2data = os.path.join(target_path, "data.npz")
        np.savez_compressed(
            path2data,
            X=X,
            y=y,
            feature_names=feature_names,  # features names
            sample_index=sample_index,  # index of samples
        )

    # save the preprocessing procedure
    saved_preprocess_steps = utilities.SavedPreprocessing(
        kept_variables=kept_variables,
        cat_variables=cat_variables,
        num_variables=num_variables,
        cat_encoder=cat_encoder,
        imputer=imputer,
    )

    return X, y, feature_names, sample_index, saved_preprocess_steps
