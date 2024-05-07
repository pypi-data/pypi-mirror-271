# -*- coding: utf-8 -*-
import importlib.metadata
import argparse


def script_validate():
    from r3xa.validation import validate
    import json

    parser = argparse.ArgumentParser(
        prog="r3xa-validate",
        description="Validate a json meta data file against the schema.",
        epilog="---",
    )
    parser.add_argument("-v", "--version", action="version", version=importlib.metadata.version("r3xa"))
    parser.add_argument(
        dest="JSON",
        type=str,
        help="path to the meta data json file to validate.",
    )
    # args parser
    args = parser.parse_args()
    instance = json.load(open(args.JSON, "r"))
    validate(instance)


def script_gui():
    from r3xa.gui import Window
    from PyQt5.QtWidgets import QApplication, QDesktopWidget
    import sys

    parser = argparse.ArgumentParser(prog="r3xa", description="Create or edit a meta data file.", epilog="---")
    parser.add_argument("-v", "--version", action="version", version=importlib.metadata.version("r3xa"))
    parser.add_argument("-j", "--json", dest="JSON", default=None, help="path to the metadata json file to edit.")
    args = parser.parse_args()

    app = QApplication(sys.argv)

    if args.JSON:
        window = Window(json_file_name=args.JSON)
    else:
        window = Window()

    screen_geometry = QDesktopWidget().screenGeometry()
    screen_height = screen_geometry.height()
    # screen_width = screen_geometry.width()
    # window.setGeometry(0, 0, int(0.3 * screen_width), int(0.9 * screen_height))
    window.setGeometry(0, 0, 720, int(0.9 * screen_height))
    window.show()

    sys.exit(app.exec())


def script_visualise():
    from r3xa.visualisation import generate_pyvis_diagram
    import json

    parser = argparse.ArgumentParser(prog="r3xa", description="Visualise a meta data file.", epilog="---")
    parser.add_argument("-v", "--version", action="version", version=importlib.metadata.version("r3xa"))
    parser.add_argument("-j", "--json", dest="JSON", type=str, help="path to the metadata json file to visualise.", required=True)
    parser.add_argument("-t", "--title", dest="TITLE", type=str, default=None, help="title of the meta data (if not given gets the name of the file).")
    args = parser.parse_args()

    instance = json.load(open(args.JSON, "r"))

    title = args.JSON[:-5] if args.TITLE is None else args.TITLE
    html_file = args.JSON.split(".json")[0] + ".html"

    # generate the diagram with a label choice ('title' ou 'id')
    network_diagram = generate_pyvis_diagram(instance, label_key=title, include_settings=1)  # ou 'id'
    network_diagram.write_html(html_file)
