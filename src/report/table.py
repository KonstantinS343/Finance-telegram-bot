import xlsxwriter

import os

from celery_app import celery
from accounting.models import OperationType
from .headers import CATEGORY, DATE, QUANTITY, OPERATION, INCOME, EXPENDITURE


@celery.task
def create_report(username: str, accounts, lang):

    data = prepare_data(accounts=accounts, lang=lang)

    workbook = xlsxwriter.Workbook(f'{os.path.dirname(__file__)}/reports/{username}_report.xlsx')
    worksheet = workbook.add_worksheet('Sheet')
    cell_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter'
    })
    worksheet.set_column(1, 4, 25)

    worksheet.write(0, 0, '№')
    worksheet.write(0, 1, CATEGORY[lang], cell_format)
    worksheet.write(0, 2, DATE[lang], cell_format)
    worksheet.write(0, 3, QUANTITY[lang], cell_format)
    worksheet.write(0, 4, OPERATION[lang], cell_format)

    for index, entry in enumerate(data):
        worksheet.write(index + 1, 0, str(index))
        worksheet.write(index + 1, 1, entry['category'], cell_format)
        worksheet.write(index + 1, 2, entry['date'])
        worksheet.write(index + 1, 3, entry['quantity'], cell_format)
        worksheet.write(index + 1, 4, entry['operation'], cell_format)

    workbook.close()


def prepare_data(accounts, lang):
    data_for_table = list()

    for i in accounts:
        item = {
            'category': i.categories,
            'date': str(i.created_at),
            'quantity': i.quantity,
            'operation': INCOME[lang] if i.operation_type == OperationType.income else EXPENDITURE[lang]
        }

        data_for_table.append(item)

    return data_for_table
