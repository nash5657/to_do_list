import csv
import inquirer

class Task:
    def __init__(self, name, description, due_date, priority):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.priority = priority


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_tasks(self):
        return self.tasks
    
    def get_task(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None
    
    def save_tasks(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'description', 'due_date', 'priority']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for task in self.tasks:
                writer.writerow({'name': task.name, 'description': task.description, 'due_date': task.due_date, 'priority': task.priority})
    def load_tasks(self, filename):
        import os
        if os.path.exists(filename):
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    task = Task(row['name'], row['description'], row['due_date'], row['priority'])
                    self.add_task(task)
        else:
            print(f"No existing tasks file found. Starting with empty task list.")

if __name__ == '__main__':
    todo_list = ToDoList()
    todo_list.load_tasks('tasks.csv')
    
    while True:
        questions = [
            inquirer.List(
                'choice',
                message="Select an option:",
                choices=['Add task', 'Remove task', 'View tasks', 'Exit'],
            )
        ]
        
        answers = inquirer.prompt(questions)
        
        if answers['choice'] == 'Add task':
            name = input("Enter task name: ")
            description = input("Enter task description: ")
            due_date = input("Enter task due date: ")
            priority = input("Enter task priority: ")
            task = Task(name, description, due_date, priority)
            todo_list.add_task(task)
            todo_list.save_tasks('tasks.csv')
            print("Task added successfully!\n")

        elif answers['choice'] == 'Remove task':
            name = input("Enter task name: ")
            task = todo_list.get_task(name)
            if task:
                todo_list.remove_task(task)
                todo_list.save_tasks('tasks.csv')
                print("Task removed successfully!\n")
            else:
                print("Task not found\n")
                
        elif answers['choice'] == 'View tasks':
            tasks = todo_list.get_tasks()
            if tasks:
                print("\nYour tasks:")
                for task in tasks:
                    print(f"Name: {task.name}, Description: {task.description}, Due Date: {task.due_date}, Priority: {task.priority}")
                print()
            else:
                print("No tasks found\n")
                
        elif answers['choice'] == 'Exit':
            todo_list.save_tasks('tasks.csv')
            print("Goodbye!")
            break
        