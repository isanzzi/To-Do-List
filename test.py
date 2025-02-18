import os
import json
import datetime
from prettytable import PrettyTable

def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

def createTodo(todos, i):
    clearTerminal()
    i += 1
    print("New TODO: ")
    newTodo = input()
    
    # Loop untuk memastikan input tanggal valid
    while True:
        deadline_str = input("Enter deadline (DD/MM/YYYY HH:MM): ")
        try:
            deadline = datetime.datetime.strptime(deadline_str, "%d/%m/%Y %H:%M")
            break  # Keluar dari loop jika format benar
        except ValueError:
            print("Format tanggal salah. Harap masukkan dalam format DD/MM/YYYY HH:MM.")
    
    dateNow = datetime.datetime.now()
    timeleft = deadline - dateNow

    todos.append(
        {
            "id": i,
            "name": newTodo,
            "deadline": deadline_str,
            "timeLeft": str(timeleft),
            "status": False,
        }
    )
    updateTodo(todos)
    return todos, i


def updateTimeLeft(todos):
    for todo in todos:
        deadline = datetime.datetime.strptime(todo["deadline"], "%d/%m/%Y %H:%M")
        dateNow = datetime.datetime.now()
        todo["timeLeft"] = str(deadline - dateNow)
    updateTodo(todos)

def updateTodo(todos):
    file = open("todo.txt", "w")
    json.dump(todos, file, indent=2)
    file.close()

def validateDeadline(new_deadline_str):
    try:
        new_deadline = datetime.datetime.strptime(new_deadline_str, "%d/%m/%Y %H:%M")
        return new_deadline
    except ValueError:
        return None

def editDeadline(todo):
    new_deadline_str = input("Ganti deadline (DD/MM/YYYY HH:MM) (tekan enter untuk tidak mengubah): ")
    
    if new_deadline_str:
        new_deadline = validateDeadline(new_deadline_str)
        if new_deadline:
            todo["deadline"] = new_deadline_str
            dateNow = datetime.datetime.now()
            todo["timeLeft"] = str(new_deadline - dateNow)
        else:
            print("Format tanggal salah. Harap masukkan dalam format DD/MM/YYYY HH:MM.")


def editTodo(todos, id):
    for todo in todos:
        if todo["id"] == id:
            new_name = input("Ganti nama TODO (tekan enter untuk tidak mengubah): ")
            if new_name:
                todo["name"] = new_name
            editDeadline(todo)

def doneTodo(todos, id):
    for todo in todos:
        if todo["id"] == id:
            todo["status"] = not todo["status"]

def getTodos(todos, idCount):
    try:
        with open("todo.txt", "r") as file:
            todos = json.load(file)
            if len(todos) != 0:
                idCount = todos[len(todos) - 1]["id"]
    except FileNotFoundError:
        # Jika file tidak ada, buat file kosong
        with open("todo.txt", "w") as file:
            json.dump([], file, indent=2)
    return todos, idCount


def printHeaderTodo(table):
    table.field_names = ["No.", "Nama", "Status", "Deadline", "Time Left"]
    return table

def printTodo(todo):
    table = PrettyTable()
    table.field_names = ["Nama", "Status", "Deadline", "Time Left"]
    table.add_row([
        todo["name"],
        "done" if todo["status"] else "not done",
        todo["timeLeft"] if todo["status"] else todo["deadline"],
        todo["timeLeft"],
    ])
    print(table)

def printTodos(todos):
    table = PrettyTable()
    print("TODO List:")
    table = printHeaderTodo(table)
    i = 1
    for todo in todos:
        table.add_row([
            i,
            todo["name"],
            "done" if todo["status"] else "not done",
            todo["timeLeft"] if todo["status"] else todo["deadline"],
            todo["timeLeft"],
        ])
        i += 1
    print(table)

def filterTodos(todos, hide):
    if hide:
        todos = [todo for todo in todos if not todo["status"]]
    return todos

def sortTodos(todos):
    todos = sorted(todos, key=lambda todo: todo["status"])
    return todos

idCount = 0
todos = []
isRunning = True
hideDone = False

while isRunning:
    todos, idCount = getTodos(todos, idCount)
    todosFiltered = filterTodos(todos, hideDone)
    todosFiltered = sortTodos(todosFiltered)
    clearTerminal()
    printTodos(todosFiltered)
    print(
        "Menu:\n- q untuk quit\n- pilih nomer untuk edit, done, atau delete\n- c untuk create\n- "
        + ("h untuk show done" if hideDone else "h untuk hide done")
    )
    menuselect = input()
    if menuselect == "q":
        isRunning = False
    elif menuselect == "c":
        todos, idCount = createTodo(todos, idCount)
    elif menuselect == "h":
        hideDone = not hideDone
    else:
        err = False
        try:
            int(menuselect)
            if (int(menuselect) > 0) and (int(menuselect) <= len(todosFiltered)):
                id = todosFiltered[int(menuselect) - 1]["id"]
                editTodo(todos, id)
        except ValueError:
            err = True
    updateTimeLeft(todos)