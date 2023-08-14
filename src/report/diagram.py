import matplotlib.pyplot as plt
import matplotlib

import os
from typing import List
from dataclasses import dataclass
from collections import defaultdict

from celery_app import celery
from accounting.models import OperationType
from .headers import INCOME, EXPENDITURE

matplotlib.use('agg')


@dataclass
class MoneyMovement():
    operation: str
    quantity: str


@celery.task
def create_diagram(username: str, accounts, lang):
    if not lang:
        lang = 'ru'
    income_data, expenditure_data = prepare_data(accounts=accounts)

    income_categories = [i for i in income_data.keys()]
    income_values = [i.quantity for i in income_data.values()]

    expenditure_categories = [i for i in expenditure_data.keys()]
    expenditure_values = [i.quantity for i in expenditure_data.values()]

    drow_diagram(path=f'{os.path.dirname(__file__)}/diagrams/{username}_income_diagram.png',
                 values=income_values,
                 categories=income_categories)

    drow_diagram(path=f'{os.path.dirname(__file__)}/diagrams/{username}_expenditure_diagram.png',
                 values=expenditure_values,
                 categories=expenditure_categories)

    drow_diagram(path=f'{os.path.dirname(__file__)}/diagrams/{username}_general_diagram.png',
                 values=[sum(income_values), sum(expenditure_values)],
                 categories=[INCOME[lang], EXPENDITURE[lang]])


def drow_diagram(path: str, values: List[float], categories: List[str]):
    if not values or (values[0] == 0 and values[1] == 0):
        plt.savefig(path)
        return
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    plt.savefig(path)
    plt.close()


def prepare_data(accounts):
    income_data = defaultdict(lambda: MoneyMovement(operation='income', quantity=0))
    expenditure_data = defaultdict(lambda: MoneyMovement(operation='expenditure', quantity=0))

    for i in accounts:
        if i.operation_type == OperationType.income:
            income_data[i.categories].quantity += i.quantity
        else:
            expenditure_data[i.categories].quantity += i.quantity

    return income_data, expenditure_data
