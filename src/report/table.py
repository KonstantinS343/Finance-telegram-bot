import xlsxwriter

import os

from celery_app import celery
from accounting.models import OperationType


@celery.task
def create_report(username: str, accounts):

    data = prepare_data(username=username, accounts=accounts)

    workbook = xlsxwriter.Workbook(f'{os.path.dirname(__file__)}/reports/{username}_report.xlsx')
    worksheet = workbook.add_worksheet('Sheet')

    worksheet.write(0, 0, '№')
    worksheet.write(0, 1, 'Name')
    worksheet.write(0, 2, 'Date')
    worksheet.write(0, 3, 'Quantity')
    worksheet.write(0, 4, 'Category')
    worksheet.write(0, 5, 'Operation')

    for index, entry in enumerate(data):
        worksheet.write(index + 1, 0, str(index))
        worksheet.write(index + 1, 1, entry['username'])
        worksheet.write(index + 1, 2, entry['date'])
        worksheet.write(index + 1, 3, entry['quantity'])
        worksheet.write(index + 1, 4, entry['category'])
        worksheet.write(index + 1, 5, entry['operation'])

    workbook.close()


def prepare_data(username: str, accounts):
    data_for_table = list()

    for i in accounts:
        item = {
            'username': username,
            'date': str(i.created_at),
            'quantity': i.quantity,
            'category': i.categories,
            'operation': 'income' if i.operation_type == OperationType.income else 'expenditure'
        }

        data_for_table.append(item)

    return data_for_table
