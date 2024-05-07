# Copyright (c) 2021 Mark Crowe <https://github.com/markcrowe-com>. All rights reserved.

import re as RegularExpression


def english_to_snake_case(name: str) -> str:
    """
    Convert English to snake_case
    :param name: string
    :return: snake_case string
    """
    return RegularExpression.sub(r'[^\w\s]', ' ', name.lower()).strip().replace(" ", "_")


def camel_to_snake_case(name: str) -> str:
    """
    Convert CamelCase to snake_case
    :param name: string
    :return: snake_case string
    """
    name: str = RegularExpression.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return RegularExpression.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def english_to_kebab_case(name: str) -> str:
    """
    Convert English to kebab case
    :param name: string
    :return: kebab case string
    """
    return name.lower().replace(" ", "-")
