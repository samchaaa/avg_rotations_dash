import gspread
import pandas as pd
from datetime import datetime
from settings import Settings


def auth():

    gc = gspread.service_account(filename=Settings.AUTH_PATH)
    sh = gc.open_by_key(Settings.SHEET_ID)

    return sh


def status():

    sh = auth()
    wks = sh.worksheet("Sheet1")

    if wks.acell("A1").value != "Currently updating":
        sh.worksheet("Sheet1").update("A1", "Currently updating")
    else:
        sh.worksheet("Sheet1").update("A1", "Last update: " + datetime.strftime(datetime.utcnow(), "%x %X"))


def write(inst, data_path):

    sh = auth()

    # Iterate through Sheet1!A2:A, if inst is not in there, add.
    wks = sh.worksheet("Sheet1")
    inst_names = wks.range('A2:A999')

    if inst not in [cell.value for cell in inst_names]:
        # find first non-blank cell
        for i, cell in enumerate(inst_names, 2):
            print(cell.value, i)
            if cell.value == "":
                wks.update('A'+str(i), inst)
                break


    data = pd.read_csv(data_path)
    header = data.columns.fillna('-').tolist()
    data = data.fillna('-').values.tolist()

    try:
        wks = sh.worksheet(inst)
    except:
        wks = sh.add_worksheet(title=inst, rows="100", cols="20")

    sh.values_clear(inst + "!A1:Z9999")

    # Update a range of cells using the top left corner address
    wks.update('A1', [header])
    wks.update('A2', data)

