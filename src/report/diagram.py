import os
import matplotlib.pyplot as plt
from typing import List
from dataclasses import dataclass

from celery_app import celery
from accounting.models import OperationType
from collections import defaultdict


@dataclass
class MoneyMovement():
    operation: str
    quantity: str


@celery.task
def create_diagram(username: str, accounts):
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


def drow_diagram(path: str, values: List[float], categories: List[str]):
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
    print(income_data)
    print(expenditure_data)

    return income_data, expenditure_data
