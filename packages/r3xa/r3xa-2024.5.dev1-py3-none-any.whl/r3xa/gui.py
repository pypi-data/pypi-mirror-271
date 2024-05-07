# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
import sys
import json
import slugify
from functools import partial

from r3xa.utils import get_schema, slugify_file_name, pprint
from r3xa.validation import validate
from r3xa.metadata import MetaData, Setting, DataSource, DataSet


class CustomTextEdit(QTextEdit):
    focusOut = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusOutEvent(self, event):
        self.focusOut.emit()
        super().focusOutEvent(event)


class CustomSpinBox(QSpinBox):
    focusOut = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.setValue(-1)
            self.clear()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.focusOut.emit()
        super().focusOutEvent(event)


class CustomDoubleSpinBox(QDoubleSpinBox):
    focusOut = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.setValue(42424242.42)
            self.clear()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.focusOut.emit()
        super().focusOutEvent(event)


def pyqtislameaf(field):
    # if isinstance(field, QLineEdit):
    #     try:
    #         return float(field.text())
    #     except Exception:
    #         return field.text()
    if isinstance(field, CustomTextEdit):
        return field.toPlainText()
    elif isinstance(field, QComboBox):
        return field.currentData()
    elif isinstance(field, CustomSpinBox):
        if not field.text():
            return None
        if int(field.value()) == -1:
            return None
        return int(field.value())
    elif isinstance(field, CustomDoubleSpinBox):
        if float(field.value()) == 42424242.42:
            return None
        if not field.text():
            return None
        return float(field.value())

    return field.text()


class Window(QDialog):
    def __init__(self, json_file_name: str = None):
        super(Window, self).__init__()

        # set output
        output = self.outputWidget()

        self.schema = get_schema()
        self.json_file_name = json_file_name
        try:
            self.json = json.load(open(self.json_file_name, "r")) if self.json_file_name else {}
        except FileNotFoundError as e:
            self.json = {}
            self.outputText.setText(str(e))
            self.outputText.setStyleSheet("color: #e22;")

        self.metadata = MetaData(payload=self.json)

        # setting window title
        self.setWindowTitle("R3XA meta data editor")

        # buid header
        header = self.headerWidget()

        # build tabs for meta data forms
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # scroll_area.setFixedHeight(False)
        tab_holder = QWidget()
        tab_layout = QVBoxLayout(tab_holder)
        self.tab_widget = QTabWidget()

        root_tab = self.rootTab()
        self.tab_widget.addTab(root_tab, "Root")

        settings_tab = self.settingsTab()
        self.tab_widget.addTab(settings_tab, "Settings")

        data_sources_tab = self.dataSourcesTab()
        self.tab_widget.addTab(data_sources_tab, "Data sources")

        data_sets_tab = self.dataSetsTab()
        self.tab_widget.addTab(data_sets_tab, "Data sets")

        json_tab = self.jsonTab()
        self.tab_widget.addTab(json_tab, "JSON")
        self.tab_widget.currentChanged.connect(self.updateTabSizes)

        tab_layout.addWidget(self.tab_widget)
        tab_holder.setLayout(tab_layout)
        scroll_area.setWidget(tab_holder)

        # save / load button
        buttons = self.buttonsWidget()

        # main layout
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(scroll_area)
        layout.addWidget(output)
        layout.addWidget(buttons)
        # layout.addStretch()

        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttons.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setLayout(layout)

    def updateTabSizes(self):
        """Resize the current tab to fit the proper vertical size"""
        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Ignored)
        policy.setVerticalPolicy(QSizePolicy.Ignored)
        for i in range(self.tab_widget.count()):
            self.tab_widget.widget(i).setSizePolicy(policy)

        policy.setVerticalPolicy(QSizePolicy.Minimum)
        current = self.tab_widget.currentWidget()
        current.setSizePolicy(policy)

    def headerWidget(self):
        header = f"""<h3>{self.schema["title"]}</h3>
        <p>{self.schema["description"]}</p>
        <p><i>Version {self.schema["properties"]["version"]["const"]}</i></p>
        <p></p>
        """
        return QLabel(header)

    def display_form_add_row(self, section_key, data_id):
        """adds a row for an array of items
        section_key: field:settings/specimen, field:data_source/specimen or field:data_set/generic
        data_id: the id slug of the data
        """
        p = self.parse_attribute(section_key)
        data_type = p["base"]  # settings, data_sources, data_sets

        # get attributes based on data_type
        layout = getattr(self, f"{data_type}_form_layout")

        self.clearLayout(layout)

        for k, widget in [(k, v) for k, v in self.__dict__.items() if self.parse_attribute(k)["base"] == data_type]:
            delattr(self, k)

        payload = [s for s in self.json[data_type] if s["id"] == data_id][0]
        self.display_form(section_key, payload, layout)

    def display_form_line(self, section_key, k, v, required, payload, layout, idx: int = None):
        """Displays a single line of the form
        section_key: something like field:settings/specimen used to setup the input attribute name
        k, v: the key value of the properties from the schema
        required: the requried field from the schema
        payload: the current value of the meta data like {'title': "I'm setting 3", 'description': 'This is my second setting', ...}
        layout: the QFormLayout
        idx: idx of the list if line is part of a list
        """

        if payload is None:
            payload = {}

        r = "*" if k in required else ""
        label = QLabel(f'<b>{v["title"]}{r}</b>')
        if r:
            label.setStyleSheet("color: #e22;")

        attribute_key = f"{section_key}/{k}"

        if idx is not None:
            attribute_key += "__" + str(idx)
            description = QHBoxLayout()
            t = QLabel(f'<i>{v["description"]}</i>')
            # b = QPushButton("Resize list")
            description.addWidget(t)
            # description.addWidget(b)
            # b.clicked.connect(partial(self.display_form_add_row, section_key, payload["id"]))
        else:
            description = QLabel(f'<i>{v["description"]}</i>')

        # if k == "kind":
        #     # ignore kind classes should be clever enough to guess it... I guess
        #     # otherwise just don't add the raw but keep the input_field
        #     return

        string_like = ["string", "number", "#/$defs/types/string", "#/$defs/types/uint"]
        # number_like = ["number", "#/$defs/types/uint"]

        if k in ["id"]:
            # handle special ID field
            pk = self.parse_attribute(section_key)
            title = f'{pk["base"].title()} -> {" -> ".join(pk["keys"])}'
            l1 = QLabel(f"<b>type [id]</b>")
            l2 = QLabel(f"{title} [{payload.get(k)}]")
            layout.addRow(l1, l2)
            setattr(self, attribute_key, QLabel(payload.get(k)))

        elif v.get("type") in string_like or v.get("$ref") in string_like:
            # handle field type and default value
            if k == "description":
                input_field = CustomTextEdit()
                input_field.setFixedHeight(150)
                input_field.setText(payload.get(k, ""))
                input_field.setTabChangesFocus(True)
                input_field.focusOut.connect(self.update_display)

            elif v.get("$ref") == "#/$defs/types/uint":
                input_field = CustomSpinBox()
                input_field.setSingleStep(1)
                input_field.setMinimum(-1)
                input_field.setMaximum(100000)
                input_field.setValue(-1)
                input_field.clear()

                try:
                    input_field.setValue(payload[k][idx])
                except KeyError:
                    pass
                except IndexError:
                    pass
                except Exception:
                    input_field.setValue(payload[k])

                input_field.focusOut.connect(self.update_display)
                if "id" in payload:  # add / remove row on the fly
                    input_field.focusOut.connect(partial(self.display_form_add_row, section_key, payload["id"]))

            elif v.get("type") == "number":
                input_field = CustomDoubleSpinBox()
                input_field.setDecimals(5)
                input_field.setMinimum(-1e10)
                input_field.setMaximum(1e10)
                input_field.setValue(424242.42)
                input_field.clear()

                try:
                    input_field.setValue(payload[k][idx])
                except KeyError:
                    pass
                except IndexError:
                    pass
                except Exception:
                    input_field.setValue(payload[k])

                input_field.focusOut.connect(self.update_display)
                if "id" in payload:  # add / remove row on the fly
                    input_field.focusOut.connect(partial(self.display_form_add_row, section_key, payload["id"]))

            else:
                input_field = QLineEdit()
                input_field.clear()

                try:  # try if list
                    input_field.setText(str(payload[k][idx]))
                except KeyError:
                    pass
                except IndexError:  # empty new line in a list
                    pass
                except Exception:  # not a list
                    input_field.setText(str(payload[k]))

                input_field.editingFinished.connect(self.update_display)
                if "id" in payload:  # add / remove row on the fly
                    input_field.editingFinished.connect(partial(self.display_form_add_row, section_key, payload["id"]))

            # handle read only
            if "const" in v:
                input_field.setText(v["const"])
                input_field.setReadOnly(True)
                input_field.setStyleSheet("color: #aaa;")

            setattr(self, attribute_key, input_field)

            if k == "kind":
                return

            if idx is None:
                layout.addRow(label, description)
                layout.addRow(input_field)
            else:
                if idx == 0:
                    layout.addRow(label, description)
                layout.addRow(QLabel(f"item {idx}"), input_field)

            # handle enum
            if isinstance(v.get("enum"), list):
                a = QLabel(f"<i>Must be one of</i>")
                b = QLabel(" or ".join([e for e in v["enum"]]))
                a.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                b.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                layout.addRow(a, b)

            # handle example
            if isinstance(v.get("examples"), list):
                a = QLabel(f"<i>e.g.</i>")
                b = QLabel(" or ".join([e for e in v["examples"]]))
                a.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                b.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                layout.addRow(a, b)

        elif v.get("$ref") in ["#/$defs/types/setting_id", "#/$defs/types/data_source_id", "#/$defs/types/data_set_id"]:
            # parse data type from $defs/types
            data_type = v["$ref"].split("/")[-1].replace("_id", "s")

            # combo box with all data
            input_field = QComboBox()
            input_field.addItem(f"--- Add existing {data_type} ---", userData="")
            input_field.model().item(0).setEnabled(False)

            # get all data_type
            all_data = getattr(self.metadata, data_type)
            item_to_see = 0
            for i, data in enumerate(all_data):
                input_field.addItem(f"{data.title} [{data.id}]", userData=data.id)

                try:
                    set_value = payload.get(k)[idx] == data.id
                except:
                    set_value = payload.get(k) == data.id

                if set_value:
                    item_to_see = i + 1

            input_field.setCurrentIndex(item_to_see)

            input_field.addItem("N/A", userData="")
            input_field.currentIndexChanged.connect(self.update_display)

            if "id" in payload:  # add / remove row on the fly
                input_field.currentIndexChanged.connect(partial(self.display_form_add_row, section_key, payload["id"]))

            setattr(self, attribute_key, input_field)

            if idx is None:
                layout.addRow(label, description)
                layout.addRow(input_field)
            else:
                if idx == 0:
                    layout.addRow(label, description)
                layout.addRow(QLabel(f"item {idx}"), input_field)

        elif v.get("$ref") in ["#/$defs/types/unit"]:
            lineEdit = QHBoxLayout()
            unit = self.schema["$defs"]["types"]["unit"]
            unit_required = unit["required"]
            for unit_k, unit_v in unit["properties"].items():
                r = "*" if unit_k in unit_required else ""
                label_unit = QLabel(f"{unit_k}{r}")
                if r:
                    label_unit.setStyleSheet("color: #e22;")
                input_field = QLineEdit()

                try:  # try if list
                    input_field.setText(str(payload[k][idx][unit_k]))
                except KeyError:
                    pass
                except IndexError:  # empty new line in a list
                    pass
                except Exception:  # not a list
                    try:
                        input_field.setText(str(payload[k][unit_k]))
                    except Exception:
                        pass

                input_field.editingFinished.connect(self.update_display)
                if "id" in payload:  # add / remove row on the fly
                    input_field.editingFinished.connect(partial(self.display_form_add_row, section_key, payload["id"]))

                attribute_key_deap = f"{attribute_key}/{unit_k}"
                setattr(self, attribute_key_deap, input_field)

                if unit_k == "kind":
                    # do not display kind
                    input_field.setText("unit")
                    continue

                lineEdit.addWidget(label_unit)
                lineEdit.addWidget(input_field)

            if idx is None:
                layout.addRow(label, description)
                layout.addRow(lineEdit)
            else:
                if idx == 0:
                    layout.addRow(label, description)
                layout.addRow(QLabel(f"item {idx}"), lineEdit)

        elif v.get("$ref") in ["#/$defs/types/data_set_file"]:
            layout.addRow(label, description)

            data_file = self.schema["$defs"]["types"]["data_set_file"]
            data_file_required = data_file["required"]
            for file_k, file_v in data_file["properties"].items():
                r = "*" if file_k in data_file_required else ""
                data_label = QLabel(f"{file_k}{r}")
                if r:
                    data_label.setStyleSheet("color: #e22;")
                input_field = QLineEdit()
                input_field.setText(str(payload.get(k, {}).get(file_k, file_v.get("default", ""))))
                input_field.editingFinished.connect(self.update_display)

                attribute_key_deap = f"{attribute_key}/{file_k}"
                setattr(self, attribute_key_deap, input_field)

                if file_k == "kind":
                    input_field.setText("data_set_file")
                    continue

                layout.addRow(data_label, input_field)

                # handle enum
                if isinstance(file_v.get("enum"), list):
                    a = QLabel(f"<i>Must be one of</i>")
                    b = QLabel(" or ".join([e for e in file_v["enum"]]))
                    a.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                    b.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                    layout.addRow(a, b)

                # handle example
                if isinstance(file_v.get("examples"), list):
                    a = QLabel(f"<i>e.g.</i>")
                    b = QLabel(" or ".join([e for e in file_v["examples"]]))
                    a.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                    b.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                    layout.addRow(a, b)

        else:
            print("NOT HANDLED", k, v)

    def display_form(self, section_key, payload, layout, ignored=[]):
        """Display the form
        section_key: something like field:settings/specimen used to setup the input attribute name
        payload: the current value of the meta data like {'title': "I'm setting 3", 'description': 'This is my second setting', ...}
        ignored: the fields from the schema we don't want to display
        layout: QFormLayout
        """

        #  the schema properties and required from the section_key
        if section_key == "field:root":
            properties = {k: v for k, v in self.schema["properties"].items() if k not in ignored}
            required = self.schema["required"]
        else:
            # print(section_key)
            if len(section_key.split("/")) > 2:
                print(f"WARNING: section key with two /: {section_key}")
            a = section_key.split("/")[0].split(":")[1]
            b = section_key.split("/")[1]
            properties = self.schema["$defs"][a][b]["properties"]
            required = self.schema["$defs"][a][b]["required"]

        # get required arguments for root parameters
        for k, v in properties.items():
            if v.get("type") in ["array"]:
                # print(section_key, k, v)
                v_array = v.copy()
                if "type" in v["items"]:
                    v_array["type"] = v["items"]["type"]
                elif "$ref" in v["items"]:
                    v_array["$ref"] = v["items"]["$ref"]
                elif "anyOf" in v["items"] and "type" in v["items"]["anyOf"][0]:
                    v_array["type"] = v["items"]["anyOf"][0]["type"]
                elif "anyOf" in v["items"] and "$ref" in v["items"]["anyOf"][0]:
                    v_array["$ref"] = v["items"]["anyOf"][0]["$ref"]
                else:
                    print("WARNING: array hasn't type or ref")
                del v_array["items"]

                # loop over the values of the payload and add one empty line
                n = len(payload.get(k, []))
                # print("copucou", payload[k])
                for i in range(n + 1):
                    self.display_form_line(section_key, k, v_array, required, payload, layout, idx=i)

            else:
                self.display_form_line(section_key, k, v, required, payload, layout)

    def rootTab(self):
        layout = QFormLayout()
        layout.addRow(QLabel("<h3>Root meta data</h3>"))

        self.json_file_name_field = QLineEdit(self.json_file_name if self.json_file_name else "")
        self.json_file_name_field.editingFinished.connect(self.onEditingFileName)
        layout.addRow(f"<b>JSON file</b>", self.json_file_name_field)

        self.display_form("field:root", self.json, layout, ignored=["settings", "data_sources", "data_sets"])

        tab = QWidget()
        tab.setLayout(layout)

        return tab

    def jsonTab(self):
        layout = QVBoxLayout()
        self.rawJson = QTextEdit()
        self.rawJson.setText(json.dumps(self.json, indent=2))
        self.rawJson.setReadOnly(True)
        self.rawJson.setAcceptRichText(True)
        self.rawJson.setStyleSheet("color: #aaa;")
        layout.addWidget(self.rawJson)

        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def set_data_combo_box(self, data_type):
        """
        data_type: settings, data_sources, data_sets
        """

        # get attribute based on data_type
        combo_box = getattr(self, f"{data_type}_combo_box")
        on_combo_box = getattr(self, f"on_{data_type}_combo_box")
        metadata = getattr(self.metadata, data_type)

        # unconnect to reset the combo box
        try:
            # print(f"disconnect {data_type} combo box", end="... ")
            combo_box.currentIndexChanged.disconnect(on_combo_box)
            # print("done")
        except TypeError as e:
            # print(f"failed ({e})")
            pass

        combo_box.clear()

        # default un triggreable
        data_type_str = data_type.replace("_", " ")
        combo_box.addItem(f"--- Manage your {data_type_str} ---", userData="MANAGE")
        combo_box.model().item(0).setEnabled(False)

        combo_box.addItem(f"--- Add new {data_type_str} ---", userData="ADD")
        combo_box.model().item(1).setEnabled(False)

        item_id = 2
        # CREATE a new settings from schema
        for k, v in self.schema["$defs"][data_type].items():
            combo_box.addItem(f"New {k}", userData=f"new_{k}")
            item_id += 1

        # EDIT get all settings from schema
        combo_box.addItem(f"--- Edit {data_type_str} ---", userData="EDIT")
        combo_box.model().item(item_id).setEnabled(False)
        item_id += 1
        for data in metadata:
            if not hasattr(data, "title"):
                setattr(data, "title", "My title")
            combo_box.addItem(f"Edit {data.title}", userData=f"edit_{data.id}")
            item_id += 1

        # DELETE get all settings from schema
        combo_box.addItem(f"--- Delete {data_type_str} ---", userData="DELETE")
        combo_box.model().item(item_id).setEnabled(False)
        item_id += 1
        for data in metadata:
            if not hasattr(data, "title"):
                setattr(data, "title", "My title")
            combo_box.addItem(f"Delete {data.title}", userData=f"delete_{data.id}")
            item_id += 1

        # reconnect again
        # print(f"connect {data_type} combo box", end="... ")
        combo_box.currentIndexChanged.connect(on_combo_box)
        # print("done")

    def settingsTab(self):
        return self.dataTab("settings")

    def dataSourcesTab(self):
        return self.dataTab("data_sources")

    def dataSetsTab(self):
        return self.dataTab("data_sets")

    def dataTab(self, data_type):
        """
        data_type: settings, data_sources, data_sets
        """
        mainLayout = QVBoxLayout()

        #######
        # Combo box to select edit/create setting
        #######

        selectLayout = QFormLayout()
        setattr(self, f"{data_type}_combo_box", QComboBox())
        combo_box = getattr(self, f"{data_type}_combo_box")
        self.set_data_combo_box(data_type)

        # setup layout
        selectLayout.addRow(combo_box)
        selectWidget = QWidget()
        selectWidget.setLayout(selectLayout)
        mainLayout.addWidget(selectWidget)

        ######
        # Form to edit/create settings
        ######
        setattr(self, f"{data_type}_form_layout", QFormLayout())

        print("data_type", data_type)

        layout = getattr(self, f"{data_type}_form_layout")
        formWidget = QWidget()
        formWidget.setLayout(layout)
        mainLayout.addWidget(formWidget)
        mainLayout.addStretch()

        tab = QWidget()
        tab.setLayout(mainLayout)
        return tab

    # we need this layer of function for the disconnect to work
    # indeed tying to disconnect partial(on_data_combo_box, "settings")) doesn't work
    def on_settings_combo_box(self, index):
        self.on_data_combo_box("settings", index)

    def on_data_sources_combo_box(self, index):
        self.on_data_combo_box("data_sources", index)

    def on_data_sets_combo_box(self, index):
        self.on_data_combo_box("data_sets", index)

    def on_data_combo_box(self, data_type, index):
        """Action when selection a setting, data_source or data_set combo box (new, edit delete)
        data_type: settings, data_sources or data_sets
        index: the position of the item in the combo box
        """
        if not index > 0:
            return

        # get attribute based on data_type
        layout = getattr(self, f"{data_type}_form_layout")
        combo_box = getattr(self, f"{data_type}_combo_box")
        metadata = getattr(self.metadata, data_type)

        # delete all self attribute of previous combo of the same type
        self.clearLayout(layout)
        for k, widget in [(k, v) for k, v in self.__dict__.items() if self.parse_attribute(k)["base"] == data_type]:
            delattr(self, k)

        key = combo_box.currentData()

        # parse key
        # new settings
        #     new_generic
        #     new_specimen
        # edit settings
        #     edit_lskhdflqsdhf
        # delete settings
        #     delete_lskhdflqsdhf

        action = key.split("_")[0]

        if action == "edit":
            data_id = "_".join(key.split("_")[1:])
            # get data from json
            data = [s for s in metadata if s.id == data_id][0]
            kind = data.kind.split("/")[1]
            section_key = f"field:{data_type}/{kind}"
            self.display_form(section_key, dict(data), layout)

            title = getattr(self, section_key + "/title")
            self.outputText.setText(f"{action.title()} {title.text()} [{data_id}]")
            self.outputText.setStyleSheet("color: #aaa;")

        elif action == "delete":
            data_id = "_".join(key.split("_")[1:])
            # remove data
            for data in [s for s in metadata if s.id == data_id]:
                self.outputText.setText(f"{data_type} {data.title} [{data.id}] deleted")

            setattr(self.metadata, data_type, [s for s in metadata if s.id != data_id])
            self.set_data_combo_box(data_type)

        elif action == "new":
            kind = "_".join(key.split("_")[1:])
            section_key = f"field:{data_type}/{kind}"
            title = f"New {kind}"
            if data_type == "settings":
                data = Setting(title=title, kind=f"{data_type}/{kind}", check=False)
            elif data_type == "data_sources":
                data = DataSource(title=title, kind=f"{data_type}/{kind}", check=False)
            elif data_type == "data_sets":
                data = DataSet(title=title, kind=f"{data_type}/{kind}", check=False)
            else:
                raise TypeError(f"No class for type {data_type}")
            self.display_form(section_key, dict(data), layout)
        else:
            print(f"action {action} is unknown (you shouldn't reach this condition)")

    def outputWidget(self):
        layout = QFormLayout()
        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setFixedHeight(50)
        layout.addRow(self.outputText)
        output = QWidget()
        output.setLayout(layout)
        return output

    def buttonsWidget(self):
        layout = QHBoxLayout()
        saveButton = QPushButton("save")
        checkButton = QPushButton("check")
        layout.addWidget(checkButton)
        layout.addWidget(saveButton)
        buttons = QWidget()
        buttons.setLayout(layout)

        checkButton.clicked.connect(self.update_display)
        saveButton.clicked.connect(self.save)
        return buttons

    def parse_attribute(self, k):
        # field:root/title                         root: True  object: False list: False
        # field:settings/specimen/title            root: False object: False list: False
        # field:settings/specimen/names__0         root: False object: False list: True
        # field:settings/specimen/size/title       root: False object: True  list: False
        # field:settings/specimen/sizes__0/title   root: False object: True  list: True

        parsed_key = {"attribute": False, "key": k, "depth": 0, "base": "", "keys": [], "array": False, "idx": 0}

        if "field:" not in k:
            return parsed_key

        # remove field
        k = k.replace("field:", "")

        # get root
        splt = k.split("/")
        parsed_key["key"] = k
        parsed_key["attribute"] = True
        parsed_key["depth"] = len(splt)
        parsed_key["base"] = splt[0]
        parsed_key["keys"] = [_.split("__")[0] for _ in splt[1:]]

        if len(splt) == 2:
            # WARNING this will break if root have lists which is not the case for now
            return parsed_key

        if "__" in splt[2]:
            # we have a list
            parsed_key["array"] = True
            parsed_key["idx"] = int(splt[2].split("__")[1])

        return parsed_key

    def update_metadata_from_fields(self):
        # print("updating metadata from fields values")

        # the payload to build and load to the self.metadata class
        # note that .load() is a delta update so not all
        # settings, data_sources and data_sets needs to be there
        # actually there can be only one of each as a tab switch from one to another

        object_selector = {"settings": {}, "data_sources": {}, "data_sets": {}}

        # the  object selector thing is just a hack to select the good object based on a string
        payload = {"settings": [object_selector["settings"]], "data_sources": [object_selector["data_sources"]], "data_sets": [object_selector["data_sets"]]}

        # loop over all attributes of the main class
        for field_key, field_value in self.__dict__.items():
            # the parsed key from the fields to navigate throught the json structure
            parsed_key = self.parse_attribute(field_key)

            # example of a parsed key which is not a list
            # {
            #     'attribute': True,
            #     'key': 'settings/specimen/description',
            #     'depth': 3,
            #     'base': 'settings',
            #     'keys': ['specimen', 'description'],
            #     'array': False,
            #     'idx': 0
            # }
            # and which is a list
            # {
            #     'attribute': True,
            #     'key': 'settings/specimen/names__1',
            #     'depth': 3,
            #     'base': 'settings',
            #     'keys': ['specimen', 'names'],
            #     'array': True,
            #     'idx': '1'
            # }

            # we ignore attributes of the class that are not fields
            if not parsed_key["attribute"]:
                continue

            # the value to set
            json_val = pyqtislameaf(field_value)

            # print(f'\t{field_key: <40}: {json_val} {type(json_val)} {"T" if json_val else "F"}')

            if parsed_key["base"] == "root":
                # we are here in the root metadata
                # for now only simple values are handled

                json_key = parsed_key["keys"][0]
                payload[json_key] = json_val

            elif parsed_key["base"] in ["settings", "data_sources", "data_sets"]:
                current_object = object_selector[parsed_key["base"]]

                # here we enter setting, data_source or data_sets
                # print(parsed_key)

                if parsed_key["array"]:
                    if parsed_key["depth"] == 3:
                        # here we have a list of simple types like
                        # settings/specimen/sizes__0/title
                        # settings/specimen/sizes__1/value

                        k1 = parsed_key["keys"][1]
                        idx = parsed_key["idx"]
                        # STEP 1: initialise the list
                        if k1 not in current_object:
                            current_object[k1] = []
                        # STEP 2: set size of the list to be at least idx (fill with "")
                        while len(current_object[k1]) < idx + 1:
                            current_object[k1].append("")
                        # STEP 3: set value to index idx of the list
                        current_object[k1][idx] = json_val

                    elif parsed_key["depth"] == 4:
                        # here we have list object type like
                        # settings/specimen/sizes__0/unit
                        # settings/specimen/sizes__1/value
                        k1 = parsed_key["keys"][1]
                        k2 = parsed_key["keys"][2]
                        idx = parsed_key["idx"]
                        # STEP 1: initialise the list
                        if k1 not in current_object:
                            current_object[k1] = []
                        # STEP 2: set size of the list to be at least idx (fill with empty dict)
                        while len(current_object[k1]) < idx + 1:
                            current_object[k1].append({})
                        # STEP 3: set value for key k2 to index idx of the list
                        current_object[k1][idx][k2] = json_val

                else:
                    if parsed_key["depth"] == 3:
                        # here we have simple type like
                        # settings/specimen/id
                        # data_sources/generic/title

                        k1 = parsed_key["keys"][1]
                        current_object[k1] = json_val

                    elif parsed_key["depth"] == 4:
                        # here we have object type like
                        # settings/specimen/size/unit
                        # settings/specimen/size/value

                        k1 = parsed_key["keys"][1]
                        k2 = parsed_key["keys"][2]
                        # STEP 1: initialise the object
                        if k1 not in current_object:
                            current_object[k1] = {}
                        # STEP 2: set value for key k2
                        current_object[k1][k2] = json_val

        # pprint(payload)
        self.metadata.load(payload)
        # print(self.metadata)
        self.json = dict(self.metadata)

        # update combo boxes
        for data_type in ["settings", "data_sources", "data_sets"]:
            # print(f"update {data_type} combo box")
            self.set_data_combo_box(data_type)

    def validate_metadata(self):
        try:
            validate(self.json)
        except Exception as e:
            print(e)
            self.outputText.setText(str(e))
            self.outputText.setStyleSheet("color: #e22;")
        else:
            self.outputText.setText("Valid JSON file")
            self.outputText.setStyleSheet("color: #2a2;")

    def update_display(self):
        self.update_metadata_from_fields()

        # edit file name if None and title set
        if self.json_file_name is None and "title" in self.json:
            self.json_file_name = slugify.slugify(self.json["title"]) + ".json"
            self.json_file_name_field.setText(self.json_file_name)

        # edit json raw
        self.rawJson.setText(json.dumps(self.json, indent=2))
        self.validate_metadata()

    def save(self):
        # update json file name
        self.update_display()  # update display if last edit is a text field
        self.json_file_name = pyqtislameaf(self.json_file_name_field)
        self.update_metadata_from_fields()

        try:
            name = self.json_file_name
            if self.json_file_name[-5:] == ".json":
                name = self.json_file_name.replace(".json", "")
            self.metadata.save_json(name=name)
            self.outputText.setText(f"JSON file saved: {name}.json")
            self.outputText.setStyleSheet("color: #2a2;")

        except Exception as e:
            print(e)
            self.outputText.setText(str(e))
            self.outputText.setStyleSheet("color: #e22;")

    def onEditingFileName(self):
        self.json_file_name = pyqtislameaf(self.json_file_name_field)
        if not len(self.json_file_name):
            self.json_file_name = None
            return

        if not self.json_file_name[-5:] == ".json":
            self.json_file_name += ".json"
        self.json_file_name = slugify_file_name(self.json_file_name)
        self.json_file_name_field.setText(self.json_file_name)

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clearLayout(item.layout())
