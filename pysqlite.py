__version__ = "2.0.0"

"""
SQLite GUI App
© 2025 KCoder Programming

Licensed under Creative Commons BY-NC 4.0
You may use, modify, and share this app, but not for commercial purposes.
More info: https://creativecommons.org/licenses/by-nc/4.0/
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QPlainTextEdit
from PySide6.QtGui import QIcon, QFont, QAction, QTextCursor, QActionGroup
from PySide6.QtCore import Qt
import sys
import json
from webbrowser import open_new_tab
import sqlite3
from tabulate import tabulate


def run_sql_query(query: str, database: str, fmt: str):
    def format_row(row):
        return ["<BLOB>" if isinstance(col, (bytes, bytearray)) else col for col in row]

    query_list = [i.replace('\n', '') for i in query.split(';') if i.strip()]
    if not query_list:
        return ">>>\n\n"
    elif 'exit' in query_list or 'exit()' in query_list:
        sys.exit()
    
    with sqlite3.connect(database, autocommit=True) as conn:
        cursor = conn.cursor()
        return_string = ""
        for query in query_list:
            try:
                cursor.execute(query)
                data1 = [format_row(row) for row in cursor.fetchall()]
                header1 = [desc[0] for desc in cursor.description if desc[0]]
                if data1:
                    if header1 and len(header1) == len(data1[0]):
                        return_string = return_string + f">>> {query}\n{tabulate(data1, header1, tablefmt=fmt)}\n\n"
                    else:
                        return_string = return_string + f">>> {query}\n{tabulate(data1, tablefmt=fmt)}\n\n"
                else:
                    return_string = return_string + f">>> {query}\nEmpty Data[]\nQuery Executed Successfully\n\n"
                
            except Exception as e:
                return_string = return_string + f">>> {query}\n{e}\n\n"
        
    return return_string

def save_settings(db_path, table_format, clear_input_checked):
    data = {"last_db": db_path, "table_format": table_format, "clear_input": clear_input_checked}
    with open(r"files\settings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_settings():
    try:
        with open(r"files\settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        save_settings("database.db", "simple_outline", False)
        return {"last_db": "database.db", "table_format": "simple_outline", "clear_input": False}

class HScrollTextEdit(QPlainTextEdit):
    def wheelEvent(self, event):
        dx_angle = event.angleDelta().x()
        dy_angle = event.angleDelta().y()

        scroll_bar = self.horizontalScrollBar()

        if dx_angle != 0:  # Traditional horizontal scroll
            scroll_bar.setValue(scroll_bar.value() - dx_angle)
        elif event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            scroll_bar.setValue(scroll_bar.value() - dy_angle)
        else:
            super().wheelEvent(event)

class NotepadWindow(QMainWindow):
    def __init__(self, file_path=None, parent=None):
        super().__init__()
        self.file_path = file_path
        self.parent_window = parent
        self.setWindowTitle("Untitled - Notepad" if not file_path else f"{file_path} - Notepad")
        self.setWindowIcon(QIcon(r"files\icon1.ico"))
        if parent:
            self.resize(parent.width()-40, parent.height()-30)
        else:
            self.resize(600, 400)

        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 13))
        self.setCentralWidget(self.editor)
        self.editor.textChanged.connect(self._mark_modified)
        self.is_modified = False
        self.editor.wheelEvent = self.wheelEvent_textinput.__get__(self)

        if self.file_path:
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(QAction("New", self, shortcut="Ctrl+N", triggered=self.new_file))
        file_menu.addAction(QAction("Open...", self, shortcut="Ctrl+O", triggered=self.open_file))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Save", self, shortcut="Ctrl+S", triggered=self.save_file))
        file_menu.addAction(QAction("Save As...", self, shortcut="Ctrl+Shift+S", triggered=self.save_file_as))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Quit", self, shortcut="Escape", triggered=self.close))

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(QAction("Undo", self, shortcut="Ctrl+Z", triggered=self.editor.undo))
        edit_menu.addAction(QAction("Redo", self, shortcut="Ctrl+Y", triggered=self.editor.redo))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Cut", self, shortcut="Ctrl+X", triggered=self.editor.cut))
        edit_menu.addAction(QAction("Copy", self, shortcut="Ctrl+C", triggered=self.editor.copy))
        edit_menu.addAction(QAction("Paste", self, shortcut="Ctrl+V", triggered=self.editor.paste))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Select All", self, shortcut="Ctrl+A", triggered=self.editor.selectAll))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction(text="Inc Size", parent=self, shortcut="Ctrl++", triggered=lambda: self.editor.zoomIn(1)))
        edit_menu.addAction(QAction(text="Dec Size", parent=self, shortcut="Ctrl+-", triggered=lambda: self.editor.zoomOut(1)))
        edit_menu.addAction(QAction(text="Reset Zoom", parent=self, shortcut="Ctrl+=", triggered=lambda: self.editor.setFont(QFont("Consolas", 13))))

        menu_bar.addAction(QAction(text="Run", parent=self, shortcut="F5", triggered=self.run))

    def _mark_modified(self):
        self.is_modified = True

    def closeEvent(self, event):
        if self.is_modified:
            reply = QMessageBox.question(self, "Save Changes?", "Do you want to save changes before closing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Yes)

            if reply == QMessageBox.StandardButton.Yes:
                result = self.save_file()
                if result:
                    if self.parent_window and self in self.parent_window.open_notepads:
                        self.parent_window.open_notepads.remove(self)
                    event.accept()
            elif reply == QMessageBox.StandardButton.No:
                if self.parent_window and self in self.parent_window.open_notepads:
                    self.parent_window.open_notepads.remove(self)
                event.accept()
            else:
                event.ignore()
        else:
            if self.parent_window and self in self.parent_window.open_notepads:
                self.parent_window.open_notepads.remove(self)
            event.accept()

    # File actions
    def new_file(self):
        reply = QMessageBox.question(self, "Confirm Action", "Do you want to save changes before closing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            result = self.save_file()
        elif reply == QMessageBox.StandardButton.No:
            result = True
        elif reply == QMessageBox.StandardButton.Cancel:
            result = False
        if result:
            self.editor.clear()
            self.setWindowTitle("Untitled - Notepad")
            self.file_path = None
            self.is_modified = False

    def open_file(self):
        reply = QMessageBox.question(self, "Confirm Action", "Do you want to save changes before closing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            result = self.save_file()
        elif reply == QMessageBox.StandardButton.No:
            result = True
        elif reply == QMessageBox.StandardButton.Cancel:
            result = False
        
        if result:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "SQL notebook (*.nbdb)")
            try:
                if file_path and file_path.endswith('.nbdb'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.editor.setPlainText(f.read())
                    self.file_path = file_path
                    self.setWindowTitle(f"{file_path} - Notepad")
                    self.is_modified = False
                elif file_path and not file_path.endswith('.nbdb'):
                    raise Exception("Different file format")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.file_path:
            if not self.file_path.endswith('.nbdb'):
                return False
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    f.write(self.editor.toPlainText())
                self.is_modified = False
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")
                return False
        else:
            return self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "SQL notebook (*.nbdb)")
        if file_path and file_path.endswith('.nbdb'):
            self.file_path = file_path
            self.save_file()
            self.setWindowTitle(f"{file_path} - Notepad")
            self.is_modified = False
            return True
        elif file_path and not file_path.endswith('.nbdb'):
            QMessageBox.critical(self, "Error", "Unable to save.")
            return False
        else:
            return False

    def run(self):
        db_path = self.parent_window.db_entry.text().strip()
        if not db_path:
            self.parent_window.output_box.insertPlainText("Error: No database selected.\n\n")
            return

        query_text = self.editor.toPlainText().strip()
        
        try:
            output = run_sql_query(query_text, db_path, self.parent_window.current_table_format)
            self.parent_window.output_box.insertPlainText(output)
            self.parent_window.output_box.moveCursor(QTextCursor.MoveOperation.End)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def wheelEvent_textinput(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.editor.zoomIn(1)
            else:
                self.editor.zoomOut(1)
        else:
            QPlainTextEdit.wheelEvent(self.editor, event)

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.open_notepads = []
        self.setWindowTitle("SQLite")
        self.setWindowIcon(QIcon(r"files\icon1.ico"))
        #self.resize(950, 600)
        self.setContentsMargins(10,0,10,10)
        self.data = load_settings()

        #menu bar setup
        menu_bar = QMenuBar(self)
        file_menu = QMenu("&File", self)
        file_menu.addAction(QAction(text="New Database", parent=self, shortcut="Ctrl+N", triggered=self.new_database))
        file_menu.addAction(QAction(text="Open Database", parent=self, shortcut="Ctrl+O", triggered=self.open_database))
        file_menu.addSeparator()
        file_menu.addAction(QAction(text="New File", parent=self, shortcut="Ctrl+Shift+N", triggered=self.new_file))
        file_menu.addAction(QAction(text="Open File", parent=self, shortcut="Ctrl+Shift+O", triggered=self.open_file))
        file_menu.addSeparator()
        file_menu.addAction(QAction(text="Quit", parent=self, shortcut="Ctrl+Q", triggered=self.close))

        edit_menu = QMenu("&Edit", self)
        self.clear_input = QAction(text="Clear Input", parent=self, shortcut="Ctrl+I", triggered=self.handle_check)
        self.clear_input.setCheckable(True)
        edit_menu.addAction(self.clear_input)
        edit_menu.addAction(QAction(text="Clear Output", parent=self, shortcut="Ctrl+K", triggered=self.clear_outp))
        edit_menu.addSeparator()
        edit_label1 = QAction(text="Input Box", parent=self)
        edit_label1.setEnabled(False)
        edit_menu.addAction(edit_label1)
        edit_menu.addAction(QAction(text="  Inc Size", parent=self, triggered=lambda: self.text_input.zoomIn(1)))
        edit_menu.addAction(QAction(text="  Dec Size", parent=self, triggered=lambda: self.text_input.zoomOut(1)))
        edit_menu.addAction(QAction(text="  Reset Zoom", parent=self, triggered=lambda: self.text_input.setFont(QFont("Consolas", 13))))
        edit_menu.addSeparator()
        edit_label2 = QAction(text="Output Box", parent=self)
        edit_label2.setEnabled(False)
        edit_menu.addAction(edit_label2)
        edit_menu.addAction(QAction(text="  Inc Size", parent=self, triggered=lambda: self.output_box.zoomIn(1)))
        edit_menu.addAction(QAction(text="  Dec Size", parent=self, triggered=lambda: self.output_box.zoomOut(1)))
        edit_menu.addAction(QAction("  Reset Zoom", self, triggered=lambda: self.output_box.setFont(QFont("Consolas", 13))))

        style_menu = QMenu("&Style", self)
        tabulate_formats = ['double_grid', 'double_outline', 'fancy_grid', 'fancy_outline', 'github', 'html', 'latex', 'mediawiki', 'moinmoin', 'orgtbl', 'grid', 'outline', 'pipe', 'plain', 'presto', 'pretty', 'psql', 'rst', 'simple', 'simple_grid', 'simple_outline', 'textile']
        style_group = QActionGroup(self)
        style_group.setExclusive(True)

        for fmt in sorted(tabulate_formats):
            action = QAction(fmt, self, checkable=True)
            if fmt == self.data.get("table_format", "simple_outline"):
                action.setChecked(True)
                self.current_table_format = fmt
            if fmt == "simple_outline":
                action.setText(f"{fmt}\t(default)")
            action.triggered.connect(lambda checked, f=fmt: self.set_table_format(f))
            
            style_group.addAction(action)
            style_menu.addAction(action) 

        help_menu = QMenu("&Help", self)
        help_menu.addAction(QAction(text="Help", parent=self, shortcut="Ctrl+H", triggered=lambda: open_new_tab(r"files\help2.html")))
        help_menu.addAction(QAction(text="SQLite", parent=self, shortcut="Ctrl+Shift+H", triggered=lambda: open_new_tab(r"files\help1.html")))
        help_menu.addAction("About", self.show_about)
        help_menu.addAction("License", self.show_license)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(style_menu)
        menu_bar.addMenu(help_menu)
        menu_bar.addAction(QAction(text="Run", parent=self, shortcut="F5", triggered=self.run_queries))
        self.setMenuBar(menu_bar)

        top_bar = QHBoxLayout()
        label1 = QLabel("SQLite")
        label1.setFont(QFont('Halveta', 16, QFont.Weight.Bold))
        top_bar.addWidget(label1)
        top_bar.addStretch()
        label2 = QLabel("\tDatabase: ")
        label2.setFont(QFont('Consolas', 13, QFont.Weight.Bold))
        top_bar.addWidget(label2)
        self.db_entry = QLineEdit("database.db", self)
        self.db_entry.setMinimumWidth(300)
        self.db_entry.setFont(QFont('Consolas', 13))
        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run_queries)
        run_button.setFont(QFont("Consolas", 13))
        top_bar.addWidget(self.db_entry)
        top_bar.addWidget(run_button)

        self.text_input = QPlainTextEdit()
        self.text_input.setPlaceholderText("Write your SQL commands here...")
        self.text_input.setFont(QFont("Consolas", 13))
        self.text_input.setFixedHeight(110)
        self.text_input.wheelEvent = self.wheelEvent_textinput.__get__(self)

        self.output_box = HScrollTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setFont(QFont("Consolas", 13))
        self.output_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        self.output_box.setMinimumHeight(200)
        
        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.text_input)
        layout.addWidget(self.output_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.db_entry.setText(self.data.get("last_db", "database.db"))
        self.clear_input.setChecked(self.data.get("clear_input", False))

    def run_queries(self):
        db_path = self.db_entry.text().strip()
        if not db_path:
            self.output_box.insertPlainText("Error: No database selected.\n\n")
            return

        query_text = self.text_input.toPlainText().strip()
        
        try:
            output = run_sql_query(query_text, db_path, self.current_table_format)
            self.output_box.insertPlainText(output)
            self.output_box.moveCursor(QTextCursor.MoveOperation.End)
            if self.clear_input.isChecked():
                self.handle_check(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        save_settings(db_path=self.db_entry.text().strip(), table_format=self.current_table_format, clear_input_checked=self.clear_input.isChecked())
        for window in self.open_notepads[:]:
            window.close()
        super().closeEvent(event)

    def set_table_format(self, fmt):
        self.current_table_format = fmt
    
    def handle_check(self, checked):
        if checked:
            self.text_input.clear()

    def clear_outp(self):
        self.output_box.clear()
        
    def new_database(self):
        file, _ = QFileDialog.getSaveFileName(self, "Create Database", "", "SQLite DB (*.db *.sqlite3)")
        if file:
            self.db_entry.setText(file)

    def open_database(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Database", "", "SQLite DB (*.db *.sqlite3)")
        if file:
            self.db_entry.setText(file)

    def new_file(self):
        notepad = NotepadWindow(parent=self)
        self.open_notepads.append(notepad)
        notepad.show()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "SQL notebook (*.nbdb)")
        try:
            if file_path and file_path.endswith('.nbdb'):
                notepad = NotepadWindow(file_path=file_path, parent=self)
                self.open_notepads.append(notepad)
                notepad.show()
            elif file_path and not file_path.endswith('.nbdb'):
                raise Exception("Different file format")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def show_about(self):
        QMessageBox.about(self, "About", "SQLite GUI App\n© 2025 KCoder-programming\nLicensed under CC BY-NC 4.0")

    def show_license(self):
        QMessageBox.about(self, "License", """Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

Copyright © 2025 KCoder Programming

You are free to:
✔ Share — copy and redistribute the material in any medium or format
✔ Adapt — remix, transform, and build upon the material

Under the following terms:
❗ Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
❗ NonCommercial — You may not use the material for commercial purposes.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

License Link: https://creativecommons.org/licenses/by-nc/4.0/""")
        
    def wheelEvent_textinput(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.text_input.zoomIn(1)
            else:
                self.text_input.zoomOut(1)
        else:
            QPlainTextEdit.wheelEvent(self.text_input, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec())
