import openpyxl.workbook
import openpyxl


def workbook_creation():
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'Top 250 movies'
    sheet.append(['Rank', "Name", "Year of release",
                  "Watchtime", "Rating", "Voted users","Image Path"])
    return excel, sheet
