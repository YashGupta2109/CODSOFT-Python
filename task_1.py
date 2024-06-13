import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


TODO_FILE = 'todo.json'


def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.tasks = load_tasks()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=15)
        self.task_listbox.pack(side=tk.LEFT, padx=10)
        self.update_listbox()

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.entry_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=10)

        self.add_button = tk.Button(self.entry_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.update_button = tk.Button(self.button_frame, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=10)

        self.toggle_button = tk.Button(self.button_frame, text="Toggle Completion", command=self.toggle_task_completion)
        self.toggle_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = '[Done]' if task['completed'] else '[Not Done]'
            self.task_listbox.insert(tk.END, f"{status} {task['description']}")

    def add_task(self):
        task_description = self.task_entry.get()
        if task_description:
            self.tasks.append({'description': task_description, 'completed': False})
            save_tasks(self.tasks)
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            new_description = simpledialog.askstring("Update Task", "Enter new task description:")
            if new_description:
                self.tasks[selected_task_index[0]]['description'] = new_description
                save_tasks(self.tasks)
                self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected. Please select a task to update.")

    def toggle_task_completion(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]['completed'] = not self.tasks[selected_task_index[0]]['completed']
            save_tasks(self.tasks)
            self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected. Please select a task to toggle.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            save_tasks(self.tasks)
            self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected. Please select a task to delete.")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
