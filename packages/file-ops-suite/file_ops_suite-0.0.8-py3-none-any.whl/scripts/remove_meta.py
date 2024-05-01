import glob
import os
import time

import win32com.client as win32


def remove_meta():
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    excel.AskToUpdateLinks = False

    filetypes = [
        "**/*.xls",
        "**/*.xlsx",
        "**/*.xlsm",
        "**/*.doc",
        "**/*.docx",
        "**/*.docm",
        "**/*.ppt",
        "**/*.pptx",
        "**/*.pptm",
    ]

    for filetype in filetypes:
        for file in glob.iglob(filetype, recursive=True):
            absolute_path = os.path.abspath(file)
            print("Working with file:", absolute_path)
            try:
                wb = excel.Workbooks.Open(absolute_path)
                time.sleep(1)
            except:
                print(
                    f"An error occurred while attempting to open the file at: {absolute_path}"
                )
                continue

            try:
                wb.RemovePersonalInformation = True
                wb.Save()
            except:
                print(
                    f"An error occurred while attempting to remove metadata at the following path: {absolute_path}"
                )
            finally:
                wb.Close()

    excel.Quit()
