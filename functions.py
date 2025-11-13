import os
import datetime as dt
import sys
import time

today = dt.date.today()
todayStr = str(today)
tomorrow = dt.date.today() + dt.timedelta(days=1)
tomorrowStr = str(tomorrow)

def createMenu():
    while True:
        clearScreen()
        print("dailyStreak \n")

        daysGoals(today)
        if completedAllGoals():
            print("\n Completed all goals, great job!\n")
        daysGoals(tomorrow)

        print("\n1. Mark goal as complete.")
        print("\n2. Add goals for tomorrow.")
        print("\nX. Exit.")

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

def daysGoals(day):
    dayStr = str(day)

    with open ("dailyGoals.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    found = False
    printing = False

    if day == today:
        print("Today's goals:")
    elif day == tomorrow:
        print("Tomorrow's goals:")

    for line in lines:
        line = line.rstrip("\n")

        if line.strip() == dayStr:
            found = True
            printing = True
            continue

        if printing and line.strip().startswith("2025-"):
            break

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

def addGoals():

    goals = input("how many goals do you want? ")
    print("Input your goals: ")
    goalList = []
    for index in range(int(goals)):
        goal = input("> ")
        goalList.append(f"{goal}")

    if os.path.isfile("dailyGoals.txt") and os.path.getsize("dailyGoals.txt") > 0:
        with open("dailyGoals.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = []

    found = False
    for index, line in enumerate(lines):
        if tomorrowStr in line:
            found = True
            newIndex = index + 1
            if newIndex < len(lines):
                existingGoals = lines[newIndex].rstrip("\n")
                newGoals = existingGoals + " " + " ".join([f"{{{goal}}}" for goal in goalList])
                lines[newIndex] = newGoals + "\n"
            else:
                lines.insert(newIndex, " ".join([f"{{{goal}}}" for goal in goalList]) + "\n")
            break

    if not found:
        lines.append(f"{tomorrowStr}\n")
        lines.append(" ".join([f"{{{goal}}}" for goal in goalList]) + "\n")

    with open("dailyGoals.txt", "w", encoding="utf-8") as file:
        file.writelines(lines)

    daysGoals(tomorrow)

def completeGoals():
    if completedAllGoals():
        print("\n What are you looking for? You completed all your goals, great job!\n")
        return
    daysGoals(today)
    print("Which goal do you want to mark as complete? If no goals completed type: 'none'")
    completedGoal = input("> ").strip()
    if completedGoal == "none":
        print("No goals have been marked as completed:")
    else:

        with open("dailyGoals.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        newLines = []
        printing = False

        for line in lines:
            stripped = line.rstrip("\n")

            if stripped == todayStr:
                printing = True
                newLines.append(stripped + "\n")
                continue

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

        daysGoals(today)

def completedAllGoals():
    with open ("dailyGoals.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    printing = False
    goalsCompleted = True

    for line in lines:
        line = line.rstrip("\n")

        if line.strip() == todayStr:
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
                    if "completed" not in word:
                        goalsCompleted = False
                    continue
                word += char

    return goalsCompleted

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")