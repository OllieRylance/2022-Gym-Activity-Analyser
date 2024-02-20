# 2022-Gym-Activity-Analyser
## Overview

Since I started going to the gym, I have kept a log of every set of exercises I have done. This is for a project like this where I analyse the information and display the data in an easy-to-digest manner.

I created two versions ("g.py" and "g - new.py") of this with functionality that I didn't end up fully completing or merging.

The outputs of the two versions of the activity analyser are shown in their respective "Page View" folders in the repository.

Now that I have found this program I have decided that I will redo the project in the future when I get the time because I still keep track of what I do and still do not have a very good method of analysing it.

## Table of Contents

- [Technical Description](#technical-description)
- [Recent Edits](#recent-edits)
- [Takeaway](#takeaway)
- [Contract Information](#contact-information)

## Technical Description

### "g.txt" - Storage

This file is filled by copying and pasting the raw Google sheet of gym data that I have into a text document. This leads to data in lines separated by tabs (\t). In both of the version of the document, the document is processed in the same way:
- Splitting the lines by tabs (\t),
- Knowing that (this is illustrated in the "google sheet example image.png"):
  - Every three columns (every three '\t's) is a new month of the sheet,
  - Every day is separated by a blank line followed by the date and type of day on one line,
- Splitting information by days based on the information above,
- Splitting days into a list of exercises containing an exercise name and information on the sets.

### "g.py" - Version 1

This version of the program goes through the dataset, works out how many times I have done certain exercises, and, based on exercise information, works out how many times I have worked certain muscle groups.

The main bulk of the code is processing the dataset and once that is complete counting is quite simple.

### "g - new.py" - Version 2

The second version of this program has more complicated features that are not in the first. The main difference is the data being represented in the form of a graph which shows how "impressive" each time I did an exercise was with what day (from day 0 being my first recorded day in the gym) it was. "Impressiveness" is measured by estimating the "one rep max" of that exercise I would have theoretically been able to do on the day, had I tried.

The graphing in the program uses "matplotlib.pyplot". The most complicated aspect of this process was putting the data into a format that the library could use.

Impressiveness (one rep max estimate) takes into account:
- General fatigue - How many exercises I had previously done that day,
- Relavent fatigue - How many sets of the current exercise I did before my most impressive set that day.

## Recent Edits
### Edits Since 2022

- Fixed a small issue with exercises that were in the dataset but not in the code.

## Takeaway
### Things I Learned from the Project

- Without proper planning, it is difficult to combine two different versions of code with different functionalities,
- How to use looping in a somewhat advanced manner to change the format of data into one that is ready for processing,
- Researching which library best solves the problem I am trying to solve (graphing in this project) before the age of ChatGPT.

## Contact Information
[LinkedIn](<https://www.linkedin.com/in/oliver-rylance-9bbb7a221/>).
