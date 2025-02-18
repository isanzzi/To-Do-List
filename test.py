import os
import json


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


def createTodo(todos, i):
    clearTerminal()
    i += 1
    print("New TODO: ")
    newTodo = input()
    todos.append({"id": i, "name": newTodo, "status": False})
    file = open("todo.json", "w")
    json.dump(todos, file)
    file.close()
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

    idCount = todos[len(todos) - 1]["id"]

    return todos, idCount


def printTodo(todo, i):
    print(
        str(i)
        + ". "
        + todo["name"]
        + " | "
        + ("done" if todo["status"] else "not done"),
    )
    i += 1
    return i


def printTodos(todos):
    print("TODO List:")
    i = 1
    for todo in todos:
        i = printTodo(todo, i)


idCount = 0
todos = []
isRunning = True
while isRunning:
    todos, idCount = getTodos(todos, idCount)
    clearTerminal()

    printTodos(todos)
    print("Menu: q untuk quit, pilih nomer untuk edit atau delete, c untuk create")
    menuselect = input()
    if menuselect == "q":
        isRunning = False
    elif menuselect == "c":
        todos, idCount = createTodo(todos, idCount)
    elif menuselect is int:
        todos, idCount = actionTodo(menuselect, todos, idCount)
