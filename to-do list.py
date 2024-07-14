import tkinter as tk
from tkinter import messagebox
import json

class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    def __str__(self):
        return f"{'[✓]' if self.completed else '[ ]'} {self.description}"

    def to_dict(self):
        return {"description": self.description, "completed": self.completed}

tasks = []

def add_task():
    description = task_entry.get()
    if description:
        tasks.append(Task(description))
        update_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Enter a task description.")

def update_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, str(task))

def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        del tasks[selected_task_index]
        update_list()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete.")

def mark_completed():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks[selected_task_index].completed = not tasks[selected_task_index].completed
        update_list()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to toggle completion.")

def update_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        new_description = task_entry.get()
        if new_description:
            tasks[selected_task_index].description = new_description
            update_list()
            task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Enter a new description for the task.")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to update.")

def load_tasks():
    global tasks
    try:
        with open('tasks.json', 'r') as file:
            tasks_data = json.load(file)
            tasks = [Task(**task) for task in tasks_data]
    except FileNotFoundError:
        tasks = []

def save_tasks():
    with open('tasks.json', 'w') as file:
        json.dump([task.to_dict() for task in tasks], file)

def main():
    global task_entry, task_listbox

    window = tk.Tk()
    window.title("To-Do List Application")
    window.configure(bg = "#D9FFDF")  
  
    load_tasks()

    #defining frames using the tk.Frame() widget  
    header_frame = tk.Frame(window, bg = "#00FF8F")
    #using the pack() method to place the frames in the application  
    header_frame.pack(fill = "both")
    header_label = tk.Label(header_frame, text = "The To-Do List", font = ("Consolas", "30"), background = "#00FF8F", foreground = "#8B4513")
    header_label.pack(padx=20, pady=20) 

    task_label = tk.Label( 
        text = "Enter the Task:",  
        font = ("Consolas", "11", "bold"),background = "#D9FFDF")  
    #using the place() method to place the label in the application  
    task_label.place(x = 10, y = 100)  
        
    task_entry = tk.Entry(window, width=70)
    task_entry.pack(padx=10, pady=10)
    
    add_button = tk.Button(window, text="Add Task",width = 20, command=add_task)
    add_button.pack(pady=5)
   
    task_listbox = tk.Listbox(window, width=50, height=10)
    task_listbox.pack(pady=10)
    update_list()
    
    update_button = tk.Button(window, text="Update Task",width = 20, command=update_task)
    update_button.pack(pady=5)
    
    delete_button = tk.Button(window, text="Delete Task",width = 20, command=delete_task)
    delete_button.pack(pady=5)
    
    mark_button = tk.Button(window, text="Mark Completed",width = 20, command=mark_completed)
    mark_button.pack(pady=5)

    window.protocol("WM_DELETE_WINDOW", lambda: (save_tasks(), window.destroy()))
    window.mainloop()

if __name__ == "__main__":
    main()
