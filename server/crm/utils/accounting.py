from crm.utils.common import debug
from typing import Optional, Union
from py_expression_eval import Parser


def calculate_by_formula(formula: str, variables: dict) -> Optional[Union[int, float]]:
    """
    Вычисляет на основе формулы

    :param str formula: Формула
    :param dict variables: Переменные которые нужно заменить в формуле
    """

    try:
        formula = formula.replace('{', '').replace('}', '').replace('ЕСЛИ', 'if').replace(',', '.').replace(';', ',')
        return Parser().parse(formula).evaluate(variables)
    except:
        return None 