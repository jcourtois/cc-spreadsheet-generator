import os
import xmltodict
import xlsxwriter

from results_objects import ProductResults

aggregated_results = {}

for root, dirs, files in os.walk("."):
    if "results.xml" in files:
        with open(os.path.join(root, "results.xml")) as single_result_file:
            single_result = xmltodict.parse(single_result_file)
            product_name = root.split('/')[-1]
            aggregated_results[product_name] = ProductResults(single_result).to_dict


workbook = xlsxwriter.Workbook('cloudcafe-results.xlsx')
worksheet = workbook.add_worksheet()

row = 0
headings = ["Product", "Test Class", "Total", "Passing Percentage",
            "Passing", "Failed", "Errored", "Skipped", "Tests failed", "Tests errored"]

for col, heading in enumerate(headings):
    worksheet.write(row, col, heading)

row = 1

for product, test_cases in aggregated_results.items():
    for test_case, result in test_cases.items():
        for col, element in enumerate([product,
                                       test_case,
                                       result["TOTAL"],
                                       result["PERCENTAGE PASSING"],
                                       result["PASSED"],
                                       result["FAILED"],
                                       result["ERROR"],
                                       result["SKIPPED"],
                                       ",".join(result["failed tests"]),
                                       ",".join(result["errored tests"])]):
            worksheet.write(row, col, element)
        row+=1

format = workbook.add_format({'bold': True, 'bg_color': '#CC7777'})

worksheet.conditional_format('D2:D{}'.format(row), {'type':     'cell',
                                                    'criteria': '<',
                                                    'value':    '1',
                                                    'format':   format})

workbook.close()
