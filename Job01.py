import json
import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog


# Composition over inheritance like efd


class Task():
        
        def __init__(self, title, description, due_date, completed, priority):
            self.__title = title
            self.__description = description
            self.__due_date =  due_date
            self.__completed = completed
            self.__priority = priority

        
        def serialize(self):
            return {
                "title": self.__title,
                "description": self.__description,
                "due_date": self.__due_date,
                "completed": self.__completed,
                "priority": self.__priority
            }


        #getter
        @property
        def title(self):
            return self.__title

        #setter
        @title.setter
        def title(self, value):
            self.__title = value

        @title.deleter
        def title(self):
            print("delete of title called")
            del self.__title

        #getter
        @property
        def description(self):
            return self.__description

        #setter
        @description.setter
        def description(self, value):
            self.__description = value

        @description.deleter
        def description(self):
            print("delete of description called")
            del self.__description
        
    
        #getter
        @property
        def due_date(self):
            return self.__due_date

        #setter
        @due_date.setter
        def due_date(self, value):
            self.__due_date = value

        @due_date.deleter
        def due_date(self):
            print("delete of due_date called")
            del self.__due_date
    

        #getter
        @property
        def completed(self):
            return self.__completed

        #setter
        @completed.setter
        def completed(self, value):
            self.__completed = value

        @completed.deleter
        def completed(self):
            print("delete of completed called")
            del self.__completed
    

        #getter
        @property
        def priority(self):
            return self.__priority

        #setter
        @priority.setter
        def priority(self, value):
            self.__priority = value

        @priority.deleter
        def priority(self):
            print("delete of priority called")
            del self.__priority

        pass
        

class TaskManager():
        
        # constructor
        def __init__(self):
            self.tasks = {}

        def show(self, opt = False):

            with open("task.json", "r") as file:
                tasks = json.load(file)  
                if opt:
                    tasks.sort( key=lambda x: x['priority'])
                     
            return tasks
        
        # ,task.description["Desc"],task.due_date["Due Date"],task.completed["Completed"],task.priority["Priority"]
        def to_csv(self):
            
            with open('task.json', encoding='utf-8') as inputfile:
                df = pd.read_json(inputfile)

            df.to_csv('csvfile.csv', encoding='utf-8', index=False)


        def add(self,task):
                
                task = task.serialize()

                tasks = []

                with open("task.json", "r") as file:
                        tasks = json.load(file) 

                # append new
                tasks.append(task)  

                #write back
                with open("task.json", "w") as file:
                        json.dump(tasks, file, indent=4)  
                        

            

        def delete(self,title):

            tasks = []
            with open("task.json", "r") as file:
                tasks= json.load(file)  

            tasks = [task for task in tasks if task['title'] != title]

        
            with open("task.json", "w") as file:
                json.dump(tasks, file, indent=4)  


        def delete_all(self):

            tasks = []
        
            with open("task.json", "w") as file:
                json.dump(tasks, file, indent=4)  



        def update(self,old_title,title,desc,date,comp,prio):
            
            tasks = task_manager.show()

            tasks = []
            with open("task.json", "r") as file:
                tasks= json.load(file)  

            for task in tasks:
                if old_title in task['title']:

                        task["title"] = title
                        task["description"] = desc
                        task["due_date"] = date
                        task["completed"] = comp
                        task["priority"] = prio
        
            with open("task.json", "w") as file:
                json.dump(tasks, file, indent=4) 

            return "updated"


task_manager = TaskManager()


def add_task():

    title = simpledialog.askstring("Input", "Title:")
    description = simpledialog.askstring("Input", "Description:")
    due_date = simpledialog.askstring("Input", "Due Date (format: DD/MM/YYYY):")
    completed = simpledialog.askstring("Input", "Completed (Y or N):")
    priority = simpledialog.askstring("Input", "Priority (1 for High, 2 for Medium, 3 for Low):")

    if all([title, description, due_date, completed, priority]):
        new_task = Task(title, description, due_date, completed, priority)
        task_manager.add(new_task)
        messagebox.showinfo("Success", "Task added successfully")
        task_manager.show()

    else:
        messagebox.showwarning("Warning", "All fields are required")

def show_tasks():
    tasks = task_manager.show()
    task_list.delete(0, tk.END)
    for task in tasks:
        formatted_task = f"{task['title']:<20} {task['description']:<15} {task['due_date']:<15}{task['completed']:<15} {task['priority']:<10}"
        task_list.insert(tk.END, formatted_task)

def show_tasks_opt():

    tasks = task_manager.show(opt = True)
    task_list.delete(0, tk.END)
    for task in tasks:
        formatted_task = f"{task['title']:<20} {task['description']:<15} {task['due_date']:<15}{task['completed']:<15} {task['priority']:<10}"
        task_list.insert(tk.END, formatted_task)


def delete_task(): 

    selected_indices = task_list.curselection()
    if selected_indices:  # Check if anything is selected
        selected_index = selected_indices[0]  # Get the first (or only) selected index
        selected_task = task_list.get(selected_index) 
        task_title = selected_task.split(" ")[0]

        messagebox.showinfo("Success", task_title)
        task_manager.delete(task_title)
        task_manager.show()

        messagebox.showinfo("Success", "Task deleted successfully")
    else:
        messagebox.showwarning("Warning", "No task selected")


def delete_all():
    del_choice = simpledialog.askstring("Input", "Delete all tasks? (Y or N): ")

    if del_choice == "Y":
        task_manager.delete_all()
        messagebox.showinfo("Warning", "All tasks deleted successfully")

def update_task():

    selected_task = task_list.get(tk.ANCHOR)
    if selected_task:
        old_title = selected_task[0]
        title = simpledialog.askstring("Input", "Title:")
        description = simpledialog.askstring("Input", "Description:")
        due_date = simpledialog.askstring("Input", "Due Date (format: DD/MM/YYYY):")
        completed = simpledialog.askstring("Input", "Completed (Y or N):")
        priority = simpledialog.askstring("Input", "Priority (1 for High, 2 for Medium, 3 for Low):")

        if all([old_title,title, description, due_date, completed, priority]):

            task = task_manager.update(old_title,title, description, due_date, completed, priority)
            if task:
                messagebox.showinfo("Success", "Task updated successfully")
            else:
                messagebox.showwarning("Warning", "Error, task noot updated")      

        else:
            messagebox.showwarning("Warning", "All fields are required")




# window
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x400") 

# widgets
add_button = tk.Button(root, text="Add Task", command=add_task)
show_button = tk.Button(root, text="Show Tasks", command=show_tasks)
delete_button = tk.Button(root, text="Delete Task", command=delete_task)
update_button = tk.Button(root, text="Update Task", command= update_task)
delete_all_button = tk.Button(root, text="Delete All Task", command=delete_all)
filter_button = tk.Button(root, text="Filter Tasks by priority", command= show_tasks_opt)
task_list = tk.Listbox(root)

add_button.pack()
show_button.pack()
delete_button.pack()
update_button.pack()
delete_all_button.pack()
filter_button.pack()
task_list.pack(fill=tk.BOTH, expand=True)

# Start the event loop
root.mainloop()



# // # CLI
        
init = ''

print("Hello what u wanna do? \n")

choice = ""

while choice != 'q':
        
        choice = input("- a: Show all tasks \n - b: Add a task \n - c: Delete a task \n - d: Update a task \n - e: Empty the task manager \n - f: filter task by priority \n - g: export to csv file \n - q: quit \n")

        if choice == "a" :

            print(task_manager.show())

        elif choice == "b" :

            b_choice = ""

            while b_choice != "q":
                task_title =  input("Insert a title for the task:")
                task_desc =  input("Insert a description for the task:")
                task_date =  input("Insert a date for the task (format: DD/MM/YYYY):")
                task_comp = input("Is the task completed? Y or N")
                task_prio = input("Which is the task priority? 1 = High, 2 = Medium, 3 = Low")

                # add validations ->

                # add task
                task = Task(task_title, task_desc, task_date, task_comp, task_prio)
                
                task_manager.add(task)


                b_choice = "q"

            # show all tasks
            choice = "a"

            


        elif choice == "c":

            task_title =  input("Insert a title of the task to be deleted:  \n 'q' to quit.")

            #with open('task.json', 'r') as file:


            task_manager.delete(task_title)

            choice = "a"

            


        elif choice == "d":
             
            old_task_title =  input("Insert a title of the task to be updated:  \n 'q' to quit. 'a' to show all tasks")
            upd_choice =""
            
            while upd_choice != "q":

                task_title =  input("Insert a title for the task:")
                task_desc =  input("Insert a description for the task:")
                task_date =  input("Insert a date for the task (format: DD/MM/YYYY):")
                task_comp = input("Is the task completed? 'Y' or 'N'")
                task_prio = input("Which is the track priority? '1' = High, '2' = Medium, '3' = Low")

                task = task_manager.update(old_task_title, task_title, task_desc,task_date,task_comp,task_prio)
                upd_choice = "q"

                if not task:
                     upd_choice = "q"

                choice = "a"
                
                


        elif choice == "e":

            #delete all
            c =  input("Do you really want to delete all the tasks? 'Y' for yes  or   'N' for no:  \n ('q' to quit. 'a' to show all tasks)")
            
            if c == "Y":
                 task_manager.delete_all()
                 print("All deleted!")
                 choice = "a"
            elif c == "q":
                 choice = "q"
            else:
                print("Nothing deleted!")
                choice = "a"
            
            
        

        elif choice == "f":

            # filter by imp
            c =  print("Task sorted by priority!")

            print(task_manager.show(opt = True))

            


        elif choice == "g":

            # filter by imp
            c =  print("Exported to csv!")

            task_manager.to_csv()

            

        
        elif choice == "q":
            choice = 'q' 
            print("Thanks, bye")





