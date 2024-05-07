# Copyright (c) 2021 Mark Crowe <https://github.com/markcrowe-com>. All rights reserved.

from code_builder.name_conventions import english_to_snake_case
from data_analytics.exploratory_data_analysis import contains_only_integer_values, is_numeric_data_type_column
from pandas import DataFrame
import os


def build_ml_data_class(dataframe: DataFrame, class_name: str = "Record") -> str:
    fields: str = ""
    values_list: str = ""
    domain_fields: str = ""

    for column_name in dataframe.columns.tolist():
        field_name: str = english_to_snake_case(column_name)

        field_type: str = ""
        field_value: str = ""

        if (is_numeric_data_type_column(dataframe[column_name])):
            field_type, field_value = ("int", "0") if (
                contains_only_integer_values(dataframe[column_name])) else ("float", "0.0")
            values_list += f"[self.{field_name}] + "
        else:
            field_type = "str"
            field_value = '""'

            domain_field_name: str = f"{field_name}_values".upper()
            domain_fields += unique_values_list_field_declaration(
                dataframe, column_name, domain_field_name)

            values_list += f"build_dummy_list({domain_field_name}, self.{field_name}) + "

        values_list = values_list.replace('] + [', ', ')
        fields += f"    {field_name}: {field_type} = {field_value}{os.linesep}"

    return f"""from data_analytics.machine_learning import build_dummy_list
from numpy import ndarray
import numpy

{domain_fields}

class {class_name}:

{fields}

    def get_values_list(self) -> list[float]:
        return {values_list[0:-3]}

    def get_values_array(self) -> ndarray[float] :
        return numpy.array(self.get_values_list()).astype(float)
"""


def unique_values_list_field_declaration(dataframe: DataFrame, column_name: str, field_name: str) -> str:
    field_declaration: str = f"{field_name}: list = ["
    for word in dataframe[column_name].unique():
        field_declaration += f'"{word}", '
    return f'{field_declaration.strip(", ")}]{os.linesep}'
