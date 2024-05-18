import sys
sys.path.append("C:\\Users\\Alexi\\anaconda3\\Lib\\site-packages\\customtkinter")
import customtkinter as ctk
from tkinter import messagebox, Listbox, END, BooleanVar
import json

# Initialize the task lists
lists = {}
current_list = None

# Save the lists to a file
def save_lists():
    with open('task_lists.json', 'w') as file:
        # Convert BooleanVar objects to boolean values before saving
        lists_to_save = {list_name: [{'title': task['title'], 'completed': task['completed'].get()} for task in tasks] for list_name, tasks in lists.items()}
        json.dump(lists_to_save, file)

# Load the lists from a file
def load_lists():
    global lists
    try:
        with open('task_lists.json', 'r') as file:
            lists_data = json.load(file)
            # Convert boolean values back to BooleanVar objects after loading
            lists = {list_name: [{'title': task['title'], 'completed': BooleanVar(value=task['completed'])} for task in tasks] for list_name, tasks in lists_data.items()}
    except FileNotFoundError:
        lists = {}

# Function to create a new list
def create_new_list():
    if len(lists) >= 3:
        messagebox.showwarning("Limit Reached", "You can only have up to 3 lists.")
        return

    new_list_window = ctk.CTkToplevel(root)
    new_list_window.title("New List")

    def save_new_list():
        list_name = list_name_entry.get()
        if list_name in lists:
            messagebox.showwarning("Duplicate Name", "A list with this name already exists.")
        elif list_name and list_name.strip():
            lists[list_name] = []
            save_lists()
            new_list_window.destroy()  # Destroy the window after saving the new list
            open_list_window(list_name)  # Open the list window after saving the new list
        else:
            messagebox.showwarning("Invalid Name", "List name cannot be empty.")

    ctk.CTkLabel(new_list_window, text="List Name:").pack(pady=10)
    list_name_entry = ctk.CTkEntry(new_list_window)
    list_name_entry.pack(pady=10)
    save_button = ctk.CTkButton(new_list_window, text="Save List", command=save_new_list)
    save_button.pack(pady=10)

def load_list():
    load_list_window = ctk.CTkToplevel(root)
    load_list_window.title("Load List")

    def load_selected_list():
        try:
            selected_list = listbox.get(listbox.curselection())
            open_list_window(selected_list)
            load_list_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load list: {e}")

    ctk.CTkLabel(load_list_window, text="Select List:").pack(pady=10)
    
    listbox_frame = ctk.CTkFrame(load_list_window)
    listbox_frame.pack(pady=10, padx=10)

    listbox = Listbox(listbox_frame)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(listbox_frame, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)

    for list_name in lists.keys():
        listbox.insert(END, list_name)

    load_button = ctk.CTkButton(load_list_window, text="Load List", command=load_selected_list)
    load_button.pack(pady=10)

def delete_list():
    delete_list_window = ctk.CTkToplevel(root)
    delete_list_window.title("Delete List")

    def delete_selected_list():
        try:
            selected_list = listbox.get(listbox.curselection())
            if selected_list:
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the list '{selected_list}'?")
                if confirm:
                    del lists[selected_list]
                    save_lists()
                    delete_list_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete list: {e}")

    ctk.CTkLabel(delete_list_window, text="Select List to Delete:").pack(pady=10)
    
    listbox_frame = ctk.CTkFrame(delete_list_window)
    listbox_frame.pack(pady=10, padx=10)

    listbox = Listbox(listbox_frame)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(listbox_frame, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)

    for list_name in lists.keys():
        listbox.insert(END, list_name)

    delete_button = ctk.CTkButton(delete_list_window, text="Delete List", command=delete_selected_list)
    delete_button.pack(pady=10)

def open_list_window(list_name):
    list_window = ctk.CTkToplevel(root)
    list_window.title(list_name)

    def add_task():
        task = task_entry.get()
        if task:
            task_completed = BooleanVar()
            task_completed.set(False)
            lists[list_name].append({'title': task, 'completed': task_completed})
            task_entry.delete(0, ctk.END)
            refresh_task_list(lists[list_name])
            save_lists()

    def refresh_task_list(tasks):
        for widget in task_frame.winfo_children():
            widget.destroy()
        for i, task in enumerate(tasks):
            task_str = task['title']
            task_completed = task['completed']
            task_checkbox = ctk.CTkCheckBox(task_frame, text=task_str, variable=task_completed)
            task_checkbox.grid(row=i, column=0, sticky='w')

    task_frame = ctk.CTkFrame(list_window)
    task_frame.pack(padx=20, pady=20)

    task_entry = ctk.CTkEntry(list_window)
    task_entry.pack(padx=20, pady=10)

    add_task_button = ctk.CTkButton(list_window, text="Add Task", command=add_task)
    add_task_button.pack(padx=20, pady=10)

    refresh_task_list(lists[list_name])

def quit_app():
    root.destroy()

# Create the main window with customtkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = ctk.CTk()
root.title("To-Do List App")

# Create the startup menu
frame = ctk.CTkFrame(root)
frame.pack(padx=20, pady=40)

new_list_button = ctk.CTkButton(frame, text="New List", command=create_new_list)
new_list_button.pack(fill=ctk.X, padx=10, pady=5)

load_list_button = ctk.CTkButton(frame, text="Load List", command=load_list)
load_list_button.pack(fill=ctk.X, padx=10, pady=5)

delete_list_button = ctk.CTkButton(frame, text="Delete List", command=delete_list)
delete_list_button.pack(fill=ctk.X, padx=10, pady=5)

quit_button = ctk.CTkButton(frame, text="Quit", command=quit_app)
quit_button.pack(fill=ctk.X, padx=10, pady=5)

# Load any existing lists
load_lists()

root.mainloop()
