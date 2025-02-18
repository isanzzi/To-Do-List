import os
import json
import datetime
# import countdown


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

    todos.append(
        {
            "id": i,
            "name": newTodo,
            "deadline": deadline_str,
            "timeLeft": str(timeleft),
            "status": False,
        }
    )
    # file = open("todo.json", "w")
    # json.dump(todos, file)
    # file.close()
    with open("todo.json", "w") as file:
        json.dump(todos, file, indent=4)
    return todos, i


def updateTodo(todos):
    file = open("todo.json", "w")
    json.dump(todos, file, indent=2)
    file.close()


# def deleteTodo(todos, todo):
#     if todo in todos:
#         file = open("todo.txt", "w")
#
def actionTodo(id, todos, idCount):
    isRunning = True
    while isRunning:
        clearTerminal()
        thisTodo = next((todo for todo in todos if todo["id"] == id), {})
        printTodo(thisTodo)
        print(
            "e untuk edit nama, d untuk delete, x untuk toggle done, q untuk kembali ke halaman utama"
        )
        menuselect = input()
        if menuselect == "e":
            editTodo(todos, id)
        # elif menuselect == "d":
        #     deleteTodo(todos, id):
        elif menuselect == "x":
            doneTodo(todos, id)
        elif menuselect == "q":
            isRunning = False

    updateTodo(todos)
    return todos, idCount


def editTodo(todos, id):
    for todo in todos:
        if todo["id"] == id:
            todo["name"] = input("Ganti nama TODO: ")


def doneTodo(todos, id):
    for todo in todos:
        if todo["id"] == id:
            todo["status"] = not todo["status"]


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
        + " | "
        + "Status"
        + " | "
        + "Deadline"
        + " | "
        + "Time left"
    )


def printTodo(todo):
    print(
        "| "
        + todo["name"]
        + " | "
        + ("done" if todo["status"] else "not done")
        + " | "
        + (todo["timeLeft"] if todo["status"] else todo["deadline"])
        + " | "
        + todo["timeLeft"]
    )
    # i += 1
    #     + ". "  # Period followed by a space for formatting
    #     + " | "  # Separator
    #     + todo["name"]  # Name of the todo item
    #     + " | "  # Separator
    #     + ("done" if todo["status"] else "not done")  # Status based on completion
    #     + " | "  # Separator
    #     + (todo["timeLeft"] if todo["status"] else todo["deadline"])  # Show time left if done, else show deadline
    #     + " |"  # Separator
    #     + todo["timeLeft"]  # Time left until deadline


def printTodos(todos):
    print("TODO List:")
    printHeaderTodo()
    i = 1
    for todo in todos:
        print(str(i) + ". ", end="")
        printTodo(todo)
        i += 1


def filterTodo(todos, hide):
    if hide:
        todos = [todo for todo in todos if not todo["status"]]
    return todos


idCount = 0
todos = []
isRunning = True
hideDone = False

# Increment the serial number for the next todo item
while isRunning:
    # Return the updated serial number
    todos, idCount = getTodos(todos, idCount)
    todosFiltered = filterTodo(todos, hideDone)
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
                todos, idCount = actionTodo(id, todos, idCount)
        except ValueError:
            err = True
            print("bruh")
