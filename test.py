import os
import json
from datetime import *
from countdown import *


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


def createTodo(todos, i):
    clearTerminal()
    i += 1
    print("New TODO: ")
    newTodo = input()
    deadline_str = input("Enter deadline (DD/MM/YYYY HH:MM): ")
    deadline = datetime.datetime.strptime(deadline_str, "%d/%m/%Y %H:%M")
    dateNow = datetime.datetime.now()
    timeleft = deadline - dateNow

    todos.append({
        "id": i,
        "name": newTodo,
        "deadline": deadline_str,
        "timeLeft": str(timeleft),
        "status": False
    })
    # file = open("todo.json", "w")
    # json.dump(todos, file)
    # file.close()
    with open("todo.json", "w") as file:
        json.dump(todos, file, indent=4)
    return todos, i


# def deleteTodo(todos, todo):
#     if todo in todos:
#         file = open("todo.txt", "w")
#
def actionTodo(id, todos, idCount):
    clearTerminal()
    print("e untuk edit nama, d untuk delete, x untuk toggle done")
    printTodo()
    menuselect = input()
    # if menuselect == 'e':
    return todos, idCount


#
# def updateTodo(todos, newTodo):
#     file = open("todo.txt", "w")
#
def getTodos(todos, idCount):
    file = open("todo.json", "r")
    todos = json.load(file)

    if len(todos) != 0:
        idCount = todos[len(todos) - 1]["id"]



    return todos, idCount


def printHeaderTodo():
    print(
        "No."
        + " | "
        + "Nama"
        + "    | "
        + "Status"
        + "   | "
        + "Deadline"
        + "         | "
        + "Time left"
    )


def printTodo(todo, i):

    print(

        str(i)
        + ". "
        + " | "
        + todo["name"]
        + " | "
        + ("done" if todo["status"] else "not done")
        + " | "
        + (todo["timeLeft"] if todo["status"] else todo["deadline"])
        + " |"
        + todo["timeLeft"] 

    )
    i += 1
        + ". "  # Period followed by a space for formatting
        + " | "  # Separator
        + todo["name"]  # Name of the todo item
        + " | "  # Separator
        + ("done" if todo["status"] else "not done")  # Status based on completion
        + " | "  # Separator
        + (todo["timeLeft"] if todo["status"] else todo["deadline"])  # Show time left if done, else show deadline
        + " |"  # Separator
        + todo["timeLeft"]  # Time left until deadline
    return i


def printTodos(todos):
    print("TODO List:")
    i = 1
    for todo in todos:
        i = printTodo(todo, i)


idCount = 0
todos = []
isRunning = True
    
    # Increment the serial number for the next todo item
while isRunning:
    return i  # Return the updated serial number
    todos, idCount = getTodos(todos, idCount)
    clearTerminal()

    printHeaderTodo()
    printTodos(todos)
    print("Menu: q untuk quit, pilih nomer untuk edit atau delete, c untuk create")
    menuselect = input()
    if menuselect == "q":
        isRunning = False
    elif menuselect == "c":
        todos, idCount = createTodo(todos, idCount)
    elif menuselect is int:
        todos, idCount = actionTodo(menuselect, todos, idCount)
