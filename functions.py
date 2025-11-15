import os
import datetime as dt
import re
import sys
import time
import calendar

# All the needed days
dayBeforeYesterday = dt.date.today() - dt.timedelta(days=2)
yesterday = dt.date.today() - dt.timedelta(days=1)
today = dt.date.today()
tomorrow = dt.date.today() + dt.timedelta(days=1)

def createMenu():  # main function of the app
    #infinite loop to have the menu always fresh
    while True:
        #clearScreen()
        #print("dailyStreak".center(50, "-"))

        # goals info cluster
        #daysGoals(today)
        if completedAllGoals(today):
            print("\nCompleted all goals, great job!")
            checkStreak(today)
        else:
            checkStreak(yesterday)
        #createCalendarGrid()
        #daysGoals(tomorrow)

        # options
        print("\n1. Mark goal as complete.")
        print("2. Add goals for tomorrow.")
        print("X. Exit.")

        # infinite function for the choices, makes it easy to backtrack in case of a miss input
        while True:
            match input("> ").strip().lower():
                case "1":
                    completeGoals()
                    break
                case "2":
                    addGoals()
                    break
                case "x":
                    print("Exiting, goodbye.")
                    sys.exit()
                case _:
                    print("Please enter a valid input.")
        time.sleep(2)


def daysGoals(day):  # shows the goals for current day
    dayStr = str(day)

    with open("dailyGoals.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    found = False
    printing = False

    if day == today:
        print("\nToday's goals:")
    elif day == tomorrow:
        print("\nTomorrow's goals:")

    # check the goals set for the sent day (today | tomorrow)
    for line in lines:
        line = line.rstrip("\n")

        # when finding the day we're looking for
        if line.strip() == dayStr:
            found = True
            printing = True
            continue

        # if we're making words, and we jump into another day
        if printing and line.strip().startswith("2025-"):
            break

        # making words
        if printing:
            word = ""
            for char in line:
                if char == "{":
                    word = " "
                    continue
                elif char == "}":
                    print(word)
                    continue
                word += char
    if day == today and not found:
        print("No goals found for today, get to writing tomorrows goals then")
    if day == tomorrow and not found:
        print("No goals found for tomorrow, do you want to add some?")


def addGoals():  # function to add goals for the next day

    goals = input("how many goals do you want? ")
    print("Input your goals: ")
    goalList = []
    for index in range(int(goals)):
        goal = input("> ")
        goalList.append(f"{goal}")

    # if the file exists open it and take it's lines into lines, if not, make lines an empty list
    if os.path.isfile("dailyGoals.txt") and os.path.getsize("dailyGoals.txt") > 0:
        with open("dailyGoals.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = []

    found = False
    # if found tomorrow's date, append new goals to old ones
    for index, line in enumerate(lines):
        if str(tomorrow) in line:
            found = True
            newIndex = index + 1
            # if our newIndex is lesser than len of lines, that means that there already are goals set for the next day
            # we append our new goals to the old ones
            if newIndex < len(lines):
                existingGoals = lines[newIndex].rstrip("\n")
                newGoals = existingGoals + " " + " ".join([f"{{{goal}}}" for goal in goalList])
                lines[newIndex] = newGoals + "\n"
            # if our index is not lesser, we insert our new goals
            else:
                lines.insert(newIndex, " ".join([f"{{{goal}}}" for goal in goalList]) + "\n")
            break
    # if we haven't found tomorrow's date, we put it in
    if not found:
        lines.append(f"{str(tomorrow)}\n")
        lines.append(" ".join([f"{{{goal}}}" for goal in goalList]) + "\n")

    with open("dailyGoals.txt", "w", encoding="utf-8") as file:
        file.writelines(lines)

    daysGoals(tomorrow)


def completeGoals():  # function for showing goal progress
    if completedAllGoals(today):
        print("\n What are you looking for? You completed all your goals, great job!\n")
        return

    #show today's goals
    daysGoals(today)
    print("Which goal do you want to mark as complete? If no goals completed type: 'none'")
    completedGoal = input("> ").strip()
    ## TODO: Make it, so that it has to match with one of the goals, otherwise make the user input once more
    if completedGoal == "none":
        print("No goals have been marked as completed:")
    else:

        with open("dailyGoals.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        newLines = []
        printing = False

        for line in lines:
            stripped = line.rstrip("\n")

            if stripped == str(today):
                printing = True
                newLines.append(stripped + "\n")
                continue

            # if we find another date, stop printing
            if printing and stripped.startswith("2025-"):
                printing = False

            if printing:
                goals = []
                word = ""
                for char in stripped:
                    if char == "{":
                        word = ""
                        continue
                    elif char == "}":
                        goalText = word.strip()
                        # if we find our completedGoal, we append (completed) to it
                        if goalText == completedGoal:
                            goalText += " (completed)"
                        goals.append(f"{{{goalText}}}")
                        continue
                    word += char
                newLines.append(" ".join(goals) + "\n")
            else:
                newLines.append(line)

        with open("dailyGoals.txt", "w", encoding="utf-8") as file:
            file.writelines(newLines)

        if completedAllGoals(today):
            checkStreak(today)
        daysGoals(today)


def completedAllGoals(day):  # function to check if all goals have been completed
    with open("dailyGoals.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    printing = False
    goalsCompleted = True

    for line in lines:
        line = line.rstrip("\n")

        if line.strip() == str(day):
            printing = True
            continue

        if printing and line.strip().startswith("2025-"):
            break

        if printing:
            word = ""
            for char in line:
                if char == "{":
                    word = ""
                    continue
                elif char == "}":
                    # we check if the goal is completed at the end of the word
                    if "completed" not in word:
                        goalsCompleted = False
                    continue
                word += char
    if printing == False:
        goalsCompleted = False
    return goalsCompleted


def clearScreen():  # function to clear the screen
    os.system("cls" if os.name == "nt" else "clear")


def checkStreak(day):  # function to check, and extend | stop count of daily goal streak
    with open("dailyStreak.txt", "a+", encoding="utf-8") as file:
        # set cursor at the start of the file
        file.seek(0)
        lines = file.readlines()

        yesterday = day - dt.timedelta(days=1)
        streak = 0

        isDayPresent = False
        # if yesterday is already present in the file, don't change the streak
        for line in lines:
            if str(day) in line:
                isDayPresent = True
                streak = streakCount(lines, day)
                break

        if isDayPresent == False:
            # if goals have been completed add a point, else set streak as 0
            streak = streakCount(lines, yesterday)
            if completedAllGoals(day):
                streak = streak + 1
            else:
                streak = 0
            file.write(f"{day} streak = {streak}\n")
    print("Your current streak is: ", streak , "\n")


def streakCount(lines, day):
    streakStr = ""
    isInside = False
    streak = 0

    for line in lines:
        # check the streak count from selected day
        if str(day) in line:
            for char in line:
                if char == "=":
                    isInside = True
                    continue
                if char == "\n":
                    isInside = False
                    continue
                if isInside:
                    streakStr += char
            streak = int(streakStr.strip())
    return streak


def loadCompletedDays():
    completedDays = set()
    datePattern = r"^\d{4}-\d{2}-\d{2}$"

    with open("dailyGoals.txt", "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    i = 0
    while i < len(lines):
        line = lines[i]

        if re.match(datePattern, line):
            currentDate = dt.datetime.strptime(line, "%Y-%m-%d").date()

            taskLine = lines[i + 1] if (i + 1) < len(lines) else ""
            tasksList = re.findall(r"\{([^}]*)\}", taskLine)

            if tasksList and all("(completed)" in task for task in tasksList):
                if currentDate.year == dt.datetime.now().year and \
                   currentDate.month == dt.datetime.now().month:
                    completedDays.add(currentDate.day)

            i += 2
        else:
            i += 1

    return completedDays


def createCalendarGrid():
    doneDays = loadCompletedDays()

    calendarDataSheet = calendar.Calendar(firstweekday=0)
    year = dt.datetime.now().year
    month = dt.datetime.now().month


    header = f"{calendar.month_name[month]} {year}"
    weekHeader = calendar.weekheader(3)
    printLines = []
    printLines.append(header.center(30))
    printLines.append(weekHeader)

    calendarMatrix = calendarDataSheet.monthdayscalendar(year, month)

    for week in calendarMatrix:
        printLine_items = []
        for day in week:
            if day == 0:
                cell = "   "
            else:
                day_str = str(day).rjust(2)
                status = "✓" if day in doneDays else " "
                cell = f"{day_str}{status}"
            printLine_items.append(cell)
        printLines.append(" ".join(printLine_items))

    print("\n".join(printLines))

