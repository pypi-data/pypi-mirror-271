"""
Machine Learning Module
Copyright © 2021 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
"""

from pandas import DataFrame
from scipy.stats import entropy

def build_dummy_list(unique_values: list, selected_item: str) -> list[int]:
    """
    Builds a dummy list with the selected item as 1 and the rest as 0.
    unique_values: list of unique values in the column
    selected_item: the item to be selected
    return: list of 0s and 1s
    """
    dummy_list: list[int] = [0 for _ in range(len(unique_values))]
    dummy_list[unique_values.index(selected_item)] = 1
    return dummy_list

def conditional_entropy(data_frame: DataFrame, feature: str, target: str) -> float:
    """Calculates the conditional entropy of a target feature given a feature H(Target|Feature)

    Args:
        data_frame (DataFrame): The data frame containing the data
        feature (str): The feature to calculate the conditional entropy for
        target (str): The target feature to calculate the conditional entropy for

    Returns:
        float: The conditional entropy of the target feature given the feature
    """
    total = 0.0
    for feature_value in data_frame[feature].unique():
        feature_value_data_frame = data_frame[data_frame[feature] == feature_value]
        feature_value_count = len(feature_value_data_frame)

        frequencies = feature_value_data_frame[target].value_counts(normalize=True)
        feature_value_entropy = entropy(frequencies, base=2)
        total += (feature_value_count / len(data_frame)) * feature_value_entropy
    return total
