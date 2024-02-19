import datetime
from math import log
import matplotlib.pyplot as plt

class spreadsheet():
    def __init__(self) -> None:
        # A dictionary of all of the exercises that I have done with the muscle group(s) that they work.
        # {exercise: [muscleGroup]}
        self.exerciseToMuslceGroup = {
            "bench press": ["chest", "~tricep"],
            "pectoral": ["chest"],
            "dip": ["chest", "~tricep"],
            "chest fly": ["chest"],
            "chest press": ["chest", "~tricep"],
            "skull crusher": ["tricep"],
            "cable push down": ["tricep"],
            "rope push down": ["tricep"],
            "close grip bench press": ["tricep", "~chest"],
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
            "sit up": ["ab"],
            "hanging leg raise": ["ab"],
            "possum": ["ab"]
        }

        # A dictionary of all of the days (including missed ones) and their activities.
        # Activities are in the form of a dictionary which contains all of the exercises and their set and rep info as a string.
        # {date: {exercise: data}}
        self.days = {}

        # A list of all of the dates which are on the spreadsheet.
        # [date]
        self.dateList = []

        # A dictionary of all of the dates with their type of day (e.g. leg day).
        # {date: type}
        self.dayTypes = {}

        # {"exercise": {date: [data, numberOfSetsDone]}}
        self.exerciseAndData = {}

    def openAndStoreFile(self) -> None:
        """Open a file that is inputted by the user and store all of the lines to 'self.fileLines'."""
        # Make sure the file entered is a file before storing its lines.
        filenameGood = False
        filename = input("What is the filename of the '.txt' file that you want to open?\n")
        while filenameGood == False:
            try:
                with open(filename + ".txt") as file:
                    self.rawLines = []
                    for line in file:
                        # Remove the new line character.
                        line = line[0:len(line) - 1]
                        self.rawLines.append(line)
                filenameGood = True
            except:
                print("Not an existing file.")
                filename = input("What is the filename of the '.txt' file that you want to open?")

    def sortOutRawLinesIntoDataPairs(self) -> None:
        numberOfMonths = len(self.rawLines[0].split("\t"))//3
        self.allDataPairsList = []
        for monthNumber in range(numberOfMonths):
            for line in self.rawLines:
                line = line.split("\t")
                monthIndex = monthNumber * 3 + 1
                # item1 is either a date or the name of an exercise.
                item1 = line[monthIndex]
                # item2 is either a day type or set and rep data.
                item2 = line[monthIndex + 1]
                if item2 != "":
                    self.allDataPairsList.append([item1, item2])

    def analyseLines(self) -> None:
        date = ""
        daysExercises = {}
        for dataPair in self.allDataPairsList:
            item1 = dataPair[0]
            item2 = dataPair[1]
            if item1 == "" and item2 != "":
                print("There is a problem with this data pair:")
                print(dataPair)
            if "/20" in item1:
                self.dateList.append(item1)
                if date:
                    self.days[date] = daysExercises
                    numberOfSetsDone = 0
                    for exercise in daysExercises:
                        if exercise not in self.exerciseAndData:
                            self.exerciseAndData[exercise] = {}
                        self.exerciseAndData[exercise][date] = [daysExercises[exercise], numberOfSetsDone]
                        numberOfSetsDone += self.returnNumberOfSets(daysExercises[exercise])
                    daysExercises = {}
                date = item1
                self.dayTypes[item1] = item2
            else:
                if item1 not in daysExercises:
                    daysExercises[item1] = item2
                else:
                    daysExercises[item1] += " + " + item2
        self.days[date] = daysExercises

    def returnTotalSetsPerExercise(self, datesInputted) -> dict:
        totalSetsPerExercise = {}
        for date in datesInputted:
            daysActivities = self.days[date]
            for exercise in daysActivities:
                sets = self.returnNumberOfSets(daysActivities[exercise])
                if exercise not in totalSetsPerExercise:
                    totalSetsPerExercise[exercise] = sets
                else:
                    totalSetsPerExercise[exercise] += sets
        return totalSetsPerExercise

    def returnNumberOfSets(self, data):
        totalSets = 0
        uniqueSets = 0
        for term in data.split(" "):
            try:
                if term[0] == "x":
                    totalSets += uniqueSets - 1
                    uniqueSets = 0
                    multipliedSets = int(term[1:len(term)])
                    totalSets += multipliedSets
                elif term != "+":
                    uniqueSets += 1
            except:
                print(" There was an error analysing this data:")
                print("|" + data + "|")
        totalSets += uniqueSets
        return totalSets

    def returnTotalSetsPerMuscleGroup(self, totalSetsPerExercise) -> dict:
        totalSetsPerMuscleGroup = {}

        for exercise in totalSetsPerExercise:
            try:
                for muscleGroup in self.exerciseToMuslceGroup[exercise]:
                    if muscleGroup[0] == "~":
                        setsToAdd = totalSetsPerExercise[exercise] // 2
                        muscleGroup = muscleGroup[1:]
                    else:
                        setsToAdd = totalSetsPerExercise[exercise]
                    if muscleGroup not in totalSetsPerMuscleGroup:
                        totalSetsPerMuscleGroup[muscleGroup] = setsToAdd
                    else:
                        totalSetsPerMuscleGroup[muscleGroup] += setsToAdd
            except:
                print(exercise)
        return totalSetsPerMuscleGroup

    def printTotalSetsPerExercise(self):
        totalSetsPerExercise = self.returnTotalSetsPerExercise(self.dateList)
        for exercise in totalSetsPerExercise:
            print(exercise, totalSetsPerExercise[exercise])

    def printTotalSetsPerMuscleGroup(self):
        totalSetsPerExercise = self.returnTotalSetsPerExercise(self.dateList)
        totalSetsPerMuscleGroup = self.returnTotalSetsPerMuscleGroup(totalSetsPerExercise)
        for muscleGroup in totalSetsPerMuscleGroup:
            print(muscleGroup, totalSetsPerMuscleGroup[muscleGroup])

    def returnScoreOfData(self, data, numberOfSetsDone = 0):
        data = data.split(" ")
        listOfSets = []
        tempSet = ""
        for item in data:
            if "x" in item:
                if item[0] != "x":
                    tempSet = item
                    listOfSets.append(item)
                else:
                    for _ in range(int(item[1:]) - 1):
                        listOfSets.append(tempSet)
        listOfScores = []
        setsOfThisExerciseDone = 0
        for set in listOfSets:
            set = set.split("x")
            set[0] = int(set[0])
            set[1] = float(set[1])
            score = set[1]
            score *= 0.025 * set[0] + 0.975
            score *= 0.02 * log(numberOfSetsDone + 1, 10) + 1
            score *= 0.07 * log(setsOfThisExerciseDone + 1, 10) + 1
            listOfScores.append(score)
            setsOfThisExerciseDone += 1
        finalScore = 0
        for score in listOfScores:
            finalScore += score
        finalScore /= len(listOfScores)
        return finalScore

    def returnDictOfDatesAndScores(self, exerciseInfo):
        dictOfDatesAndScores = {}
        for date in exerciseInfo:
            dictOfDatesAndScores[date] = s1.returnScoreOfData(exerciseInfo[date][0], exerciseInfo[date][1])
        return dictOfDatesAndScores

    def printDatesAndScoresOfExercise(self, exercise):
        exerciseInfo = self.exerciseAndData[exercise]
        scores = self.returnDictOfDatesAndScores(exerciseInfo)
        for date in scores:
            print(date, round(scores[date], 1))

    def graphScoreOfExercise(self):
        exercise = input("Name the exercise which you wish to be graphed.\n")
        exerciseInfo = self.exerciseAndData[exercise]
        scores = self.returnDictOfDatesAndScores(exerciseInfo)
        dayZeroDate = self.dateList[0]
        year = int(dayZeroDate[6:10])
        month = int(dayZeroDate[3:5])
        day = int(dayZeroDate[0:2])
        formattedDayZeroDate = datetime.datetime(year, month, day)
        xCoordinates = []
        yCoordinates = []
        for date in scores:
            year = int(date[6:10])
            month = int(date[3:5])
            day = int(date[0:2])
            formattedDate = datetime.datetime(year, month, day)
            dayNumber = (formattedDate - formattedDayZeroDate).days
            xCoordinates.append(dayNumber)
            yCoordinates.append(scores[date])
        plt.plot(xCoordinates, yCoordinates)
        plt.ylabel("Score")
        plt.xlabel("Day Number")
        plt.show()

    def menu(self):
        print("""File opened and analysed.
        
What would you like to do with the file? Your options are:
    1) """)

    def main(self) -> None:
        print("Welcome to the work out analyst.")
        self.openAndStoreFile()
        self.sortOutRawLinesIntoDataPairs()
        self.analyseLines()
        self.menu()
        # for day in self.days:
        #     print(self.days[day])
        # for date in self.dayTypes:
        #     print(self.dayTypes[date])
        # self.printTotalSetsPerExercise()
        # self.printTotalSetsPerMuscleGroup()
        # self.printDatesAndScoresOfExercise("bench press")
        self.graphScoreOfExercise()


s1 = spreadsheet()
s1.main()