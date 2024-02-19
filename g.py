import datetime

def addSets(exercise, data, totalSetsPerExercise):
    sets = 0
    loneSets = 0
    for term in data.split(" "):
        if term[0] == "x":
            sets += loneSets - 1
            termSets = term[1:len(term)]
            sets += int(termSets)
            loneSets = 0
        elif term != "+":
            loneSets += 1
    sets += loneSets
    totalSetsPerExercise[exercise] += sets
    return totalSetsPerExercise

def analyseLines(lines, days, dateList, dayTypes):
    #temp variables for making "days" dict + othersa
    day = ""
    daysExercises = {}
    for line in lines:
        #removes "\n"
        line = line[0:len(line)-1]
        splitLine = line.split("\t")
        column1 = splitLine[1]
        column2 = splitLine[2].strip()
        #if is date
        if "/20" in column1:
            day = column1
            dayTypes[column1] = column2
        #if is a month title
        elif " 20" in column1:
            pass
        #if is a blank line
        elif column1 ==  "" and column1 == "":
            #if day exists add to dictionary of days; else wait until a day
            if day:
                days[day] = daysExercises
                dateList.append(day)
                day = ""
                daysExercises = {}
            else:
                pass
        #this is just exercises and 
        else:
            if column2:
                daysExercises[column1] = column2
    return days, dateList, dayTypes

def addToTotalSetsPerExercise(days, totalSetsPerExercise, dateList):
    #reset totalSetsPerExercise
    for exercise in totalSetsPerExercise:
        totalSetsPerExercise[exercise] = 0

    for date in dateList:
        for exercise in days[date]:
            try:
                totalSetsPerExercise = addSets(exercise, days[date][exercise], totalSetsPerExercise)
            except:
                print("problem with adding to totalSetsPerExercise")
                print(date, exercise, days[date][exercise])
    return totalSetsPerExercise

def addToTotalSetsPerMuscleGroup(totalSetsPerExercise, totalSetsPerMuscleGroup, exerciseToMuslceGroup):
    #reset totalSetsPerExercise
    for muscleGroup in totalSetsPerMuscleGroup:
        totalSetsPerMuscleGroup[muscleGroup] = 0

    for exercise in totalSetsPerExercise:
        for muscleGroup in exerciseToMuslceGroup[exercise]:
            if muscleGroup[0] == "~":
                totalSetsPerMuscleGroup[muscleGroup[1:]] += totalSetsPerExercise[exercise] // 2
            else:
                totalSetsPerMuscleGroup[muscleGroup] += totalSetsPerExercise[exercise]
    return totalSetsPerMuscleGroup

def dataBetweenDates(days, totalSetsPerExercise, totalSetsPerMuscleGroup, exerciseToMuslceGroup, dateList):
    formattedDateList = {

    }

    for date in dateList:
        year = int(date[6:10])
        month = int(date[3:5])
        day = int(date[0:2])
        formattedDate = datetime.datetime(year, month, day)
        formattedDateList[date] = formattedDate

    print("data between date1 and date2 (inclusive)")
    date1 = input("date1 (dd/mm/yyyy)\n")
    year1 = int(date1[6:10])
    month1 = int(date1[3:5])
    day1 = int(date1[0:2])
    date2 = input("date2 (dd/mm/yyyy)\n")
    year2 = int(date2[6:10])
    month2 = int(date2[3:5])
    day2 = int(date2[0:2])

    newDateList = []

    for date in formattedDateList:
        if formattedDateList[date] >= datetime.datetime(year1, month1, day1) and formattedDateList[date] <= datetime.datetime(year2, month2, day2):
            newDateList.append(date)
    
    addToTotalSetsPerExercise(days, totalSetsPerExercise, newDateList)
    addToTotalSetsPerMuscleGroup(totalSetsPerExercise, totalSetsPerMuscleGroup, exerciseToMuslceGroup)

def displayTotalSetsPerExercise(totalSetsPerExercise):
    print("exercise followed by number of sets:")
    for exercise in totalSetsPerExercise:
        if totalSetsPerExercise[exercise]:
            print(exercise, totalSetsPerExercise[exercise])

def displayTotalSetsPerMuscleGroup(totalSetsPerMuscleGroup):
    print("muscle group followed by number of sets:")
    for muscleGroup in totalSetsPerMuscleGroup:
        if totalSetsPerMuscleGroup[muscleGroup]:
            print(muscleGroup, totalSetsPerMuscleGroup[muscleGroup])

def main():
    with open('g.txt') as file:
        lines = [line[0:len(line) - 1] for line in file]

    #{date: {exercise: data}}
    days = {}

    #[date]
    dateList = []

    #{date: type}
    dayTypes = {}

    #{exercise: totalSetsDone}
    totalSetsPerExercise = {
        "bench press": 0,
        "pectoral": 0,
        "dip": 0,
        "chest press": 0,
        "skull crusher": 0,
        "cable push down": 0,
        "rope push down": 0,
        "shoulder press": 0,
        "lateral raise": 0,
        "shrug": 0,
        "cable lateral raise": 0,
        "overhead press": 0,
        "preacher curl": 0,
        "cable curl": 0,
        "chin up": 0,
        "bicep curl": 0,
        "close grip pull down": 0,
        "low row": 0,
        "pull up": 0,
        "reverse fly": 0,
        "lateral pull down": 0,
        "deadlift": 0,
        "barbell row": 0,
        "forearm": 0,
        "leg extension": 0,
        "leg press": 0,
        "abductor": 0,
        "adductor": 0,
        "calf raise": 0,
        "squat": 0,
        "bulgarian squat": 0,
        "leg curl": 0,
        "abdominal crunch": 0,
        "russian twist": 0,
        "sit up w/ weight": 0,
        "hanging leg raise": 0,
        "possum": 0,
        "sit up": 0,
        "chest fly": 0,
        "close grip bench press": 0
    }

    #{muscleGroup: totalSetsDone}
    totalSetsPerMuscleGroup = {
        "chest": 0,
        "back": 0,
        "bicep": 0,
        "tricep": 0,
        "ab": 0,
        "quad": 0,
        "hamstring": 0,
        "glutes": 0,
        "calf": 0,
        "shoulder": 0,
        "forearm": 0,
        "trap": 0
    }
    
    #{exercise: [muscleGroup]}
    exerciseToMuslceGroup = {
        "bench press": ["chest", "~tricep"],
        "pectoral": ["chest"],
        "dip": ["chest", "~tricep"],
        "chest press": ["chest", "~tricep"],
        "skull crusher": ["tricep"],
        "cable push down": ["tricep"],
        "rope push down": ["tricep"],
        "shoulder press": ["shoulder", "~tricep"],
        "lateral raise": ["shoulder"],
        "shrug": ["trap"],
        "cable lateral raise": ["shoulder"],
        "overhead press": ["shoulder", "~tricep"],
        "preacher curl": ["bicep"],
        "cable curl": ["bicep"],
        "chin up": ["bicep", "back"],
        "bicep curl": ["bicep"],
        "close grip pull down": ["bicep", "back"],
        "low row": ["bicep", "back"],
        "pull up": ["~bicep", "back"],
        "reverse fly": ["back", "shoulder", "~trap"],
        "lateral pull down": ["~bicep", "back"],
        "deadlift": ["~quad", "~hamstring", "glutes", "~trap", "back"],
        "barbell row": ["back", "trap", "~bicep", "~forearm"],
        "forearm": ["forearm"],
        "leg extension": ["quad"],
        "leg press": ["quad", "hamstring", "glutes"],
        "abductor": ["~glutes"],
        "adductor": ["~glutes"],
        "calf raise": ["calf"],
        "squat": ["quad", "hamstring", "glutes", "back", "~calf"],
        "bulgarian squat": ["quad", "hamstring", "glutes"],
        "leg curl": ["hamstring"],
        "abdominal crunch": ["ab"],
        "russian twist": ["ab"],
        "sit up w/ weight": ["ab"],
        "hanging leg raise": ["ab"],
        "possum": ["ab"],
        "sit up": ["ab"],
        "chest fly": ["chest"],
        "close grip bench press": ["chest", "~tricep"]
    }

    #loop for reformatting and analsysing the spreadsheet
    numMonths = len(lines[0].split("\t"))//3
    monthList = []
    for month in range(numMonths):
        for line in lines:
            line = line.split("\t")
            monthList.append("\t".join([line[3*month], line[3*month + 1], line[3*month + 2]])+"\t")
    analyseLines(monthList, days, dateList, dayTypes)

    #the programs user interface start
    timeScale = input("what time period? all (a) / between dates (bd)\n")
    if timeScale != "bd":
        addToTotalSetsPerExercise(days, totalSetsPerExercise, dateList)
        addToTotalSetsPerMuscleGroup(totalSetsPerExercise, totalSetsPerMuscleGroup, exerciseToMuslceGroup)
    else:
        dataBetweenDates(days, totalSetsPerExercise, totalSetsPerMuscleGroup, exerciseToMuslceGroup, dateList)
    
    #the programs output
    dataType = input("what type of data? exercises (ex) / muscle groups worked (mgw) / both (b)\n")
    print()
    if dataType == "ex":
        displayTotalSetsPerExercise(totalSetsPerExercise)
    elif dataType == "mgw":
        displayTotalSetsPerMuscleGroup(totalSetsPerMuscleGroup)
    else:
        displayTotalSetsPerExercise(totalSetsPerExercise)
        print()
        displayTotalSetsPerMuscleGroup(totalSetsPerMuscleGroup)

main()