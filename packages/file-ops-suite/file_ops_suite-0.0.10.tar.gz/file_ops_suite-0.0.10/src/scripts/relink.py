import argparse
import time

from pywinauto.application import Application


def relink():
    parser = argparse.ArgumentParser(
        "relink",
        "Relink file in Power Bi dashboard",
    )
    parser.add_argument("--to-gdrive", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.to_gdrive:
        path = r"G:\My Drive\work\STO_lab\Power BI and data Aug 2023\data"
    else:
        path = r"C:\Users\boris.garbuzov\OneDrive - Skilled Trades Ontario\Desktop\boris\power bi\data"

    app = Application(backend="uia").connect(path="PBIDesktop.exe")
    pb = app.window()
    pb.set_focus()
    sources = pb.ListBox2.wrapper_object()
    change_source_btn = pb.child_window(title="Change Source...", control_type="Text")

    for source in sources:
        if not args.to_gdrive:
            source.set_focus().click_input()
        change_source_btn.click_input()
        edit_path = pb.child_window(title="File path", control_type="Edit")
        path_part = edit_path.get_value().split("data")[-1]
        edit_path.set_text(path + path_part)
        pb.child_window(title="OK", control_type="Button").click_input()
        time.sleep(2)

    pb.child_window(title="Close", control_type="Text").click_input()
