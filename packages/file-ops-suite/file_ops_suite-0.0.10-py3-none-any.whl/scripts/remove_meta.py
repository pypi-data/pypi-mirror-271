import glob
import os
import time

import win32com.client as win32


def initialize_application(
    application_name, visible=True, ask_to_update=True, display_alerts=True
):
    app = win32.gencache.EnsureDispatch(application_name)
    if visible:
        app.Visible = False
    if ask_to_update:
        app.AskToUpdateLinks = False
    if display_alerts:
        app.DisplayAlerts = False
    return app


def remove_meta():
    excel = initialize_application("Excel.Application")
    power_point = initialize_application("PowerPoint.Application", False, False)
    word = initialize_application("Word.Application", ask_to_update=False)

    apps = {"Excel": excel, "PowerPoint": power_point, "Word": word}

    filetypes = {
        "Excel": ["**/*.xls", "**/*.xlsx", "**/*.xlsm"],
        "PowerPoint": ["**/*.ppt", "**/*.pptx", "**/*.pptm"],
        "Word": ["**/*.doc", "**/*.docx", "**/*.docm"],
    }

    for app_name, app in apps.items():
        for filetype in filetypes[app_name]:
            for file in glob.iglob(filetype, recursive=True):
                absolute_path = os.path.abspath(file)
                print("Working with file:", absolute_path)
                try:
                    if app_name == "Excel":
                        doc = app.Workbooks.Open(absolute_path)
                    elif app_name == "PowerPoint":
                        doc = app.Presentations.Open(absolute_path, WithWindow=False)
                    else:
                        doc = app.Documents.Open(absolute_path)
                    time.sleep(1)
                    doc.RemovePersonalInformation = True
                    doc.Save()
                except Exception:
                    print(f"Error occurred while processing file: {absolute_path}")
                    continue
                finally:
                    doc.Close()

    for app in apps.values():
        app.Quit()
