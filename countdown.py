import datetime

def input_goal():
    goal = input(" Enter your goal : ")
    return goal

def input_time():
    time = input(" Enter the date of your goal in the format 'dd/mm/yyyy' ")
    return time

def print_goal(goal):
    print("Your goal is to " + goal)

def print_input_time(time):
    print("The date of your goal is " + time + " ")

def now():
    now = datetime.datetime.now()
    return now

def goal_time(time):
    goal_time = datetime.datetime.strptime(time, "%d/%m/%Y")
    return goal_time

def print_goal_time(goal_time):
    print("The date of your goal is " + goal_time + " ")

def time_left(goal_time, now):
    time_left = goal_time - now
    return time_left

def print_time_left(time_left):
    print(f"Time left to reach your goal is {time_left} ")

def check_time_left(time_left):
    if time_left.days < 0:
        print("The date has passed")
        print(f"Time passed since your goal is {-time_left.days} days")
    elif time_left.days == 0:
        print("The date is today")
    else:
        print(f"Time left to reach your goal is {time_left} ")

def write_goal_to_file(goal):  
    with open("goal.txt", "w") as file:
        file.write(goal)

def write_time_to_file(time):
    with open("time.txt", "w") as file:
        file.write(time)

def write_time_left_to_file(time_left):
    with open("time_left.txt", "w") as file:
        file.write(time_left)

# input_goal = input(" Enter your goal : ")
# input_time = input(" Enter the date of your goal in the format 'dd/mm/yyyy' ")


# goal_time = datetime.datetime.strptime(input_time, "%d/%m/%Y")
# now = datetime.datetime.now()

# time_left = goal_time - now

# if time_left.days < 0:
#     print("The date has passed")
#     print(f"Time passed since your goal is {-time_left.days} days")
# elif time_left.days == 0:
#     print("The date is today")
# else:
#     print(f"Time left to reach your goal is {time_left} ")