
import os
from datetime import datetime, date
from dateutil import parser

# Constants
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to register a new user
def reg_user(username_password):
    """Register a new user."""
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Username already exists. Please choose a different username.")
            continue
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            with open("user.txt", "a") as out_file:
                out_file.write(f"\n{new_username};{new_password}")
            break
        else:
            print("Passwords do not match")

# Function to add a new task
def add_task(task_list, username_password):
    """Add a new task."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = parser.parse(task_due_date)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:
        str_attrs = [
            new_task['username'],
            new_task['title'],
            new_task['description'],
            new_task['due_date'].strftime("%Y-%m-%d"),
            new_task['assigned_date'].strftime("%Y-%m-%d"),
            "No"
        ]
        task_file.write("\n" + ";".join(str_attrs))
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    """View all tasks."""
    if not task_list:
        print("No tasks available.")
        return
    for idx, t in enumerate(task_list, start=1):
        disp_str = f"Task {idx}:\n"
        disp_str += f"Title: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += f"Date Assigned: {t['assigned_date'].strftime('%Y-%m-%d')}\n"
        disp_str += f"Due Date: {t['due_date'].strftime('%Y-%m-%d')}\n"
        disp_str += f"Task Description:\n{t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(task_list, curr_user):
    """View tasks assigned to the current user."""
    tasks_assigned_to_user = [t for t in task_list if t['username'] == curr_user]
    if not tasks_assigned_to_user:
        print("No tasks assigned to you.")
        return
    while True:
        print("Tasks assigned to you:")
        for idx, t in enumerate(tasks_assigned_to_user, start=1):
            print(f"{idx}. {t['title']} - Due: {t['due_date'].strftime('%Y-%m-%d')}")

        choice = input("Enter task number to select task, or '-1' to return to main menu: ")
        if choice == '-1':
            return
        try:
            task_idx = int(choice) - 1
            selected_task = tasks_assigned_to_user[task_idx]
            print(f"Selected Task: {selected_task['title']}")
            action = input("Do you want to mark this task as complete (type 'complete') or edit this task (type 'edit'): ")
            if action == 'complete':
                selected_task['completed'] = True
                print("Task marked as complete.")
            elif action == 'edit':
                edit_option = input("What do you want to edit? (username/due_date): ").lower()
                if edit_option == 'username':
                    new_username = input("Enter new username: ")
                    selected_task['username'] = new_username
                    print("Username updated.")
                elif edit_option == 'due_date':
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                    selected_task['due_date'] = datetime.strptime(new_due_date, "%Y-%m-%d")
                    print("Due date updated.")
                else:
                    print("Invalid edit option.")
            else:
                print("Invalid choice.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid task number.")

# Function to generate reports
def generate_reports(task_list, username_password):
    """Generate reports."""
    if not task_list:
        print("No tasks available to generate reports.")
        return

    # Task Overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < date.today())

    # Avoid division by zero error
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0

    with open("task_overview.txt", "w") as report_file:
        report_file.write("Task Overview\n")
        report_file.write(f"Total tasks: {total_tasks}\n")
        report_file.write(f"Completed tasks: {completed_tasks}\n")
        report_file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        report_file.write(f"Overdue tasks: {overdue_tasks}\n")
        report_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        report_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    # Print the generated report
    with open("task_overview.txt", "r") as report_file:
        print(report_file.read())

    # User Overview
    total_users = len(username_password)
    with open("user_overview.txt", "w") as report_file:
        report_file.write("User Overview\n")
        report_file.write(f"Total users: {total_users}\n")
        for username in username_password:
            user_tasks = [t for t in task_list if t['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'].date() < date.today())
            if total_user_tasks > 0:
                percentage_assigned = (total_user_tasks / total_tasks) * 100
                percentage_completed = (completed_user_tasks / total_user_tasks) * 100
                percentage_incomplete = (incomplete_user_tasks / total_user_tasks) * 100
                percentage_overdue = (overdue_user_tasks / total_user_tasks) * 100
            else:
                percentage_assigned = 0
                percentage_completed = 0
                percentage_incomplete = 0
                percentage_overdue = 0
            report_file.write(f"\nUser: {username}\n")
            report_file.write(f"Total tasks assigned: {total_user_tasks}\n")
            report_file.write(f"Percentage of total tasks assigned: {percentage_assigned:.2f}%\n")
            report_file.write(f"Percentage of completed tasks: {percentage_completed:.2f}%\n")
            report_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
            report_file.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n")
    print("Reports generated successfully.")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Read task data from tasks.txt
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    if not t_str:
        continue  # Skip empty lines
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    if len(task_components) != 6:
        print("Invalid data format in tasks.txt:", t_str)
        continue  # Skip lines with incorrect format

    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]

    # Attempt to parse the due date in both formats
    try:
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    except ValueError:
        try:
            # Try parsing with an alternative date format
            curr_t['due_date'] = datetime.strptime(task_components[3], "%Y.%m.%d")
        except ValueError:
            print("Invalid date format in tasks.txt:", t_str)
            continue  # Skip lines with incorrect date format

    # Attempt to parse the assigned date in both formats
    try:
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    except ValueError:
        try:
            # Try parsing with an alternative date format
            curr_t['assigned_date'] = datetime.strptime(task_components[4], "%Y.%m.%d")
        except ValueError:
            print("Invalid date format in tasks.txt:", t_str)
            continue  # Skip lines with incorrect date format

    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if not user:
        continue  # Skip empty lines
    user_info = user.split(';')
    if len(user_info) != 2:
        print("Invalid data format in user.txt:", user)
        continue  # Skip lines with incorrect format
    username, password = user_info
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task(task_list, username_password)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list, curr_user)

    elif menu == 'ds':
        if curr_user == 'admin':
            # Display statistics
            # Modify the menu option that allows the admin to display statistics
            # so that the reports generated are read from tasks.txt and user.txt
    
            if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
                # If these text files don’t exist (because the user hasn’t selected to generate them yet),
                # first call the code to generate the text files
                print("Generating required text files...")
                # Code to generate the text files can be added here
                print("Text files generated successfully.")
            generate_reports(task_list, username_password)
        else:
            print("You don't have permission to access this option.")

    elif menu == 'gr':
        if curr_user == 'admin':
            generate_reports(task_list, username_password)
        else:
            print("You don't have permission to access this option.")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")