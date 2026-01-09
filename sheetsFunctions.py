import gspread
import pandas as pd

def get_sheet(client, id):
    return client.open_by_key(id)

def get_worksheet(sheet, title):
    return sheet.worksheet(title)

def get_worksheet_columns(worksheet):
    data = worksheet.get_all_values()
    rows = data[1:]

    urls = [row[0] for row in rows]
    mentions = [row[1] for row in rows]
    channels = [row[2] for row in rows]
    files = [row[3] for row in rows]

    return urls, mentions, channels, files

def update_worksheet_logs(worksheet, update):
    new_row = [update]
    worksheet.append_row(new_row)