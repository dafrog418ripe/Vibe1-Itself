import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

TASKS_FILE = 'tasks.json'
PRIORITIES = ["None", "Low", "Medium", "High"]

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.tasks = []
        self.load_tasks()
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        # Set minimum window size
        self.root.minsize(500, 350)
        # Frame for adding tasks
        add_frame = ttk.Frame(self.root)
        add_frame.pack(pady=10)

        ttk.Label(add_frame, text="Task:").grid(row=0, column=0)
        self.task_entry = ttk.Entry(add_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)
        self.task_entry.focus_set()  # Focus entry on startup
        self.task_entry.bind('<Return>', lambda event: self.add_task())  # Enter to add

        ttk.Label(add_frame, text="Priority:").grid(row=0, column=2)
        self.priority_var = tk.StringVar(value=PRIORITIES[0])
        self.priority_menu = ttk.Combobox(add_frame, textvariable=self.priority_var, values=PRIORITIES, state="readonly", width=8)
        self.priority_menu.grid(row=0, column=3, padx=5)

        add_btn = ttk.Button(add_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=0, column=4, padx=5)

        # Task list
        self.tree = ttk.Treeview(self.root, columns=("Task", "Priority", "Status"), show="headings", selectmode="browse")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Mark Complete/Incomplete", command=self.toggle_complete).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        priority = self.priority_var.get()
        if not task_text:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            self.task_entry.focus_set()
            return
        self.tasks.append({
            "task": task_text,
            "priority": priority if priority != "None" else "",
            "completed": False
        })
        self.save_tasks()
        self.refresh_tasks()
        self.task_entry.delete(0, tk.END)
        self.priority_var.set(PRIORITIES[0])
        self.task_entry.focus_set()  # Refocus after adding

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Edit Task", "Please select a task to edit.")
            return
        idx = int(selected[0])
        task = self.tasks[idx]
        new_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task["task"])
        if new_task is not None and new_task.strip():
            new_priority = simpledialog.askstring("Edit Priority (Low, Medium, High, or leave blank)", "Edit priority:", initialvalue=task["priority"])
            if new_priority is not None:
                if new_priority not in PRIORITIES and new_priority != "":
                    messagebox.showwarning("Input Error", "Priority must be Low, Medium, High, or blank.")
                    return
                self.tasks[idx]["task"] = new_task.strip()
                self.tasks[idx]["priority"] = new_priority if new_priority != "None" else ""
                self.save_tasks()
                self.refresh_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete Task", "Please select a task to delete.")
            return
        idx = int(selected[0])
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            del self.tasks[idx]
            self.save_tasks()
            self.refresh_tasks()

    def toggle_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Toggle Complete", "Please select a task.")
            return
        idx = int(selected[0])
        self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
        self.save_tasks()
        self.refresh_tasks()

    def refresh_tasks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, task in enumerate(self.tasks):
            status = "Complete" if task["completed"] else "Incomplete"
            priority = task["priority"] if task["priority"] else "None"
            self.tree.insert("", "end", iid=str(idx), values=(task["task"], priority, status))

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
    root = tk.Tk()
    # Set ttk theme for macOS compatibility
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except:
        pass
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 