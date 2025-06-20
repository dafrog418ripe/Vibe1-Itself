import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QMessageBox, QHeaderView, QAbstractItemView, QLabel,
    QInputDialog
)
from PyQt5.QtCore import Qt

TASKS_FILE = 'tasks.json'
PRIORITIES = ["Low", "Medium", "High"]

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.resize(600, 400)
        self.tasks = []
        self.load_tasks()
        self.init_ui()
        self.refresh_table()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add task controls
        add_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task...")
        self.priority_input = QComboBox()
        self.priority_input.addItems(PRIORITIES)
        self.priority_input.setCurrentText("Medium")
        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_task)
        add_layout.addWidget(QLabel("Task:"))
        add_layout.addWidget(self.task_input)
        add_layout.addWidget(QLabel("Priority:"))
        add_layout.addWidget(self.priority_input)
        add_layout.addWidget(add_btn)
        layout.addLayout(add_layout)

        # Task table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Task", "Priority", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table)

        # Action buttons
        btn_layout = QHBoxLayout()
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_task)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_task)
        toggle_btn = QPushButton("Mark Complete/Incomplete")
        toggle_btn.clicked.connect(self.toggle_complete)
        sort_btn = QPushButton("Sort by Priority")
        sort_btn.clicked.connect(self.sort_by_priority)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(toggle_btn)
        btn_layout.addWidget(sort_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def add_task(self):
        text = self.task_input.text().strip()
        priority = self.priority_input.currentText()
        if not text:
            QMessageBox.warning(self, "Input Error", "Task cannot be empty.")
            return
        self.tasks.append({
            "task": text,
            "priority": priority,
            "completed": False
        })
        self.save_tasks()
        self.refresh_table()
        self.task_input.clear()
        self.priority_input.setCurrentText("Medium")

    def edit_task(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Edit Task", "Please select a task to edit.")
            return
        task = self.tasks[row]
        text, ok = QInputDialog.getText(self, "Edit Task", "Edit task:", text=task["task"])
        if ok and text.strip():
            priority, ok2 = QInputDialog.getItem(self, "Edit Priority", "Edit priority:", PRIORITIES, PRIORITIES.index(task["priority"] if task["priority"] else "Medium"), False)
            if ok2:
                self.tasks[row]["task"] = text.strip()
                self.tasks[row]["priority"] = priority
                self.save_tasks()
                self.refresh_table()

    def delete_task(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Delete Task", "Please select a task to delete.")
            return
        reply = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.tasks[row]
            self.save_tasks()
            self.refresh_table()

    def toggle_complete(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Toggle Complete", "Please select a task.")
            return
        self.tasks[row]["completed"] = not self.tasks[row]["completed"]
        self.save_tasks()
        self.refresh_table()

    def sort_by_priority(self):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        self.tasks.sort(key=lambda t: priority_order.get(t["priority"], 3))
        self.save_tasks()
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for task in self.tasks:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(task["task"]))
            self.table.setItem(row, 1, QTableWidgetItem(task["priority"]))
            status = "Complete" if task["completed"] else "Incomplete"
            item = QTableWidgetItem(status)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 2, item)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=2)

def main():
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 