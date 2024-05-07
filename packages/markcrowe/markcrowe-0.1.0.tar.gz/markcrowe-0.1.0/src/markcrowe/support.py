"""
Copyright (c) 2021 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
"""

import pickle
from numpy import ndarray
from sklearn.preprocessing import MinMaxScaler


class FileOpenModes:
    """File open modes"""

    APPEND: str = "a"
    BINARY: str = "b"
    EXCLUSIVE: str = "x"
    READ: str = "r"
    TEXT: str = "t"
    UPDATING: str = "+"
    WRITE: str = "w"

    APPEND_BINARY: str = "ab"
    APPEND_TEXT: str = "at"

    READ_BINARY: str = "rb"
    READ_TEXT: str = "rt"

    WRITE_BINARY: str = "wb"
    WRITE_TEXT: str = "wt"


def scale_fit_save_transform(
    training_data: ndarray, testing_data: ndarray, scaler_filepath: str, scaler=None
) -> tuple[ndarray, ndarray, any]:
    """Scale, fit, save and transform data.
    Fit the scaler to the training data and then transform the training and testing data.
    Save the scaler to a file.
    Return the transformed training and testing data.
    """
    if scaler is None:
        scaler = MinMaxScaler()

    scaler.fit(training_data)

    with open(scaler_filepath, FileOpenModes.WRITE_BINARY) as file:
        pickle.dump(scaler, file)

    return scaler.transform(training_data), scaler.transform(testing_data), scaler
