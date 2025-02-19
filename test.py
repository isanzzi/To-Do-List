import os
import json
import datetime
from prettytable import PrettyTable


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


def actionTodo(id, todos):
    isRunning = True
    while isRunning:
        clearTerminal()
        thisTodo = next((todo for todo in todos if todo["id"] == id), {})
        # if thisTodo:
        printTodo(thisTodo)
        print(
            "Menu:\n- e untuk edit nama\n- d untuk delete\n- x untuk toggle done\n- q untuk kembali ke halaman utama"
        )
        menuselect = input()
        if menuselect == "e":
            editTodo(thisTodo, todos)
        elif menuselect == "d":
            todos = deleteTodo(todos, thisTodo)
            isRunning = False
        elif menuselect == "x":
            doneTodo(todos, thisTodo)
        elif menuselect == "q":
            isRunning = False
        # else:
        #     isRunning = False
    updateTodo(todos)
    return todos


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

    while True:
        prioritas = input("Tingkat prioritas (1 = least priority, 5 = max priority): ")
        try:
            prioritas = int(prioritas)
            if 1 <= prioritas <= 5:
                break
            else:
                print("Input tidak valid")
        except ValueError:
            print("Input tidak valid")
    todos.append(
        {
            "id": i,
            "name": newTodo,
            "deadline": deadline_str,
            "timeLeft": str(timeleft),
            "prioritas": prioritas,
            "status": False,
        }
    )
    updateTodo(todos)
    return todos, i


def deleteTodo(todos, todo):
    if todo in todos:
        todos = [todo1 for todo1 in todos if todo1 != todo]
        updateTodo(todos)

    return todos


def updatestodostatus(todos, todo):
    for i, todo in enumerate(todos, start=1):
        print(f"{i}. {todo['name']} | {'done' if todo['status'] else 'not done'}")


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
    new_deadline_str = input(
        "Ganti deadline (DD/MM/YYYY HH:MM) (tekan enter untuk tidak mengubah): "
    )

    if new_deadline_str:
        new_deadline = validateDeadline(new_deadline_str)
        if new_deadline:
            todo["deadline"] = new_deadline_str
            dateNow = datetime.datetime.now()
            todo["timeLeft"] = str(new_deadline - dateNow)
        else:
            print("Format tanggal salah. Harap masukkan dalam format DD/MM/YYYY HH:MM.")
    editPrioritas(todo)


def editPrioritas(todo):
    prioritas = input("Tingkat prioritas (1 = least priority, 5 = max priority): ")
    if prioritas:
        try:
            prioritas = int(prioritas)
            if 1 <= prioritas <= 5:
                todo["prioritas"] = prioritas
            else:
                print("Input tidak valid")
        except ValueError:
            print("Input tidak valid")


def editTodo(todo, todos):
    clearTerminal()
    printTodo(todo)
    if todo in todos:
        new_name = input("Ganti nama TODO (tekan enter untuk tidak mengubah): ")
        if new_name:
            todo["name"] = new_name
        editDeadline(todo)


def doneTodo(todos, todo):
    if todo in todos:
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
    table.field_names = ["No.", "Nama", "Status", "Prioritas", "Deadline", "Time Left"]
    return table


def printTodo(todo):
    table = PrettyTable()
    table.field_names = ["Nama", "Status", "Prioritas", "Deadline", "Time Left"]
    table.add_row(
        [
            todo["name"],
            "done" if todo["status"] else "not done",
            todo["prioritas"],
            todo["deadline"],
            todo["timeLeft"],
        ]
    )
    print(table)


def printTodos(todos):
    table = PrettyTable()
    print("TODO List:")
    table = printHeaderTodo(table)
    i = 1
    for todo in todos:
        table.add_row(
            [
                i,
                todo["name"],
                "done" if todo["status"] else "not done",
                todo["prioritas"],
                todo["deadline"],
                todo["timeLeft"],
            ]
        )
        i += 1
    print(table)


def filterTodos(todos, hide):
    if hide:
        todos = [todo for todo in todos if not todo["status"]]
    return todos


def sortSelect():
    clearTerminal()
    print("Pilih metode sortir:")
    print("1. Default (not done dulu)")
    print("2. Berdasarkan tanggal (terdekat dulu)")
    print("3. Berdasarkan tanggal (terjauh dulu)")
    print("4. Berdasarkan prioritas (tertinggi dulu)")
    print("5. Berdasarkan prioritas (terendah dulu)")
    pilihan = input("Masukkan nomor metode sortir: ")
    return pilihan


def sortTodos(todos, pilihan):
    if pilihan == "2":
        todos.sort(
            key=lambda x: datetime.datetime.strptime(x["deadline"], "%d/%m/%Y %H:%M")
        )
    elif pilihan == "3":
        todos.sort(
            key=lambda x: datetime.datetime.strptime(x["deadline"], "%d/%m/%Y %H:%M"),
            reverse=True,
        )
    elif pilihan == "4":
        todos.sort(key=lambda x: x["prioritas"], reverse=True)
    elif pilihan == "5":
        todos.sort(key=lambda x: x["prioritas"])
    else:
        todos = sorted(todos, key=lambda todo: todo["status"])
    return todos


idCount = 0
todos = []
isRunning = True
hideDone = False
sortMode = 1

while isRunning:
    todos, idCount = getTodos(todos, idCount)
    todosFiltered = filterTodos(todos, hideDone)
    todosFiltered = sortTodos(todosFiltered, sortMode)
    clearTerminal()
    printTodos(todosFiltered)
    print(
        "Menu:\n- q untuk quit\n- pilih nomer untuk edit, done, atau delete\n- c untuk create\n- "
        + ("h untuk show done" if hideDone else "h untuk hide done")
        + "\n- s untuk pilih metode sorting"
    )
    menuselect = input()
    if menuselect == "q":
        isRunning = False
    elif menuselect == "c":
        todos, idCount = createTodo(todos, idCount)
    elif menuselect == "h":
        hideDone = not hideDone
    elif menuselect == "s":
        sortMode = sortSelect()
    else:
        err = False
        try:
            int(menuselect)
            if (int(menuselect) > 0) and (int(menuselect) <= len(todosFiltered)):
                id = todosFiltered[int(menuselect) - 1]["id"]
                todos = actionTodo(id, todos)
        except ValueError:
            err = True
    updateTimeLeft(todos)
