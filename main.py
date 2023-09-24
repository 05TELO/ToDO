import sys
from PyQt5 import QtWidgets, QtCore
import sqlite3


class CustomButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self.setMouseTracking(True)
        self.setStyleSheet(
            """
            QPushButton {
                width: 500;
                height: 25;
                color: #FFFFFF;
                background-color: #1E90FF;
            }

            QPushButton:hover {
                cursor: pointer;
                background-color: #6495ED;
                color: #FFFFFF;
            }
        """
        )

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        super().leaveEvent(event)


class BazaListsApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect("todo.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            lists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)
            """
        )

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ToDo App")
        self.setGeometry(300, 300, 750, 300)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(50, 25, 50, 50)
        layout.setSpacing(20)

        self.label = QtWidgets.QLabel("Daily Tasks")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        font = self.label.font()
        font.setPointSize(25)
        font.setBold(True)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.entry = QtWidgets.QLineEdit()
        self.entry.setPlaceholderText("Add todo")
        self.entry.setFixedSize(500, 25)
        layout.addWidget(self.entry)

        self.listbox = QtWidgets.QListWidget()
        self.listbox.setFixedSize(500, 150)
        layout.addWidget(self.listbox)

        self.button_add = CustomButton("Add")
        self.button_add.clicked.connect(self.add_list)
        layout.addWidget(self.button_add)

        self.button_update = CustomButton("Update")
        self.button_update.clicked.connect(self.update_list)
        layout.addWidget(self.button_update)

        self.button_remove = CustomButton("Delete")
        self.button_remove.clicked.connect(self.remove_list)
        layout.addWidget(self.button_remove)

        self.setLayout(layout)

        self.load_lists()

        self.show()

    def add_list(self):
        name = self.entry.text().strip()
        if name:
            self.cur.execute("INSERT INTO lists (name) VALUES (?)", (name,))
            self.conn.commit()
            self.listbox.addItem(name)
            self.entry.clear()

    def update_list(self):
        selected_item = self.listbox.currentItem()
        if selected_item:
            name = self.entry.text().strip()
            if name:
                new_item = QtWidgets.QListWidgetItem(name)
                self.listbox.insertItem(
                    self.listbox.row(selected_item), new_item
                )
                self.listbox.takeItem(self.listbox.row(selected_item))
                self.cur.execute(
                    "UPDATE lists SET name=? WHERE name=?",
                    (name, selected_item.text()),
                )
                self.conn.commit()
                self.entry.clear()

    def remove_list(self):
        selected_item = self.listbox.currentItem()
        if selected_item:
            name = selected_item.text()
            self.cur.execute("DELETE FROM lists WHERE name=?", (name,))
            self.conn.commit()
            self.listbox.takeItem(self.listbox.row(selected_item))

    def load_lists(self):
        self.cur.execute("SELECT name FROM lists")
        for row in self.cur.fetchall():
            name = row[0]
            self.listbox.addItem(name)

    def closeEvent(self, event):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    baza_lists_app = BazaListsApp()
    sys.exit(app.exec_())
