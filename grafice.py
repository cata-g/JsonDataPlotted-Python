import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import collections
file = open("file.json")
data = json.load(file)
plt.rcParams['font.size'] = 5


def stringToDate(date, time):
    if date != "" and time != "":
        timeString = date + ' ' + time[:-5]
        timeObject = datetime.strptime(timeString, "%m/%d/%Y %H:%M:%S")
        if time[len(time)-5:] == " p.m.":
            timeObject += timedelta(hours=12)
        return timeObject
    else:
        return ""


def getData(index):
    actions = {}
    for i in data:
        if i['ID'] > index:
            break
        if i["ID"] == index:
            if i["Action number"] != 0:
                startDate = stringToDate(
                    i["Actual Start Date of Process"], i["Actual Start Time of Process"])
                endDate = stringToDate(
                    i["Actual End Date of Process"], i["Actual End Time of Process"])
                seconds = (endDate-startDate).total_seconds()
                minutes = seconds/60
                actions[i["Action number"]] = minutes

    actionNames = {}
    for i in data:
        actionNames[i["Action"]] = i['Action number']

    names = []
    values = []
    for key in sorted(actions):
        names.append(key)
        values.append(actions[key])
    for name in range(len(names)):
        for key in actionNames:
            if names[name] == actionNames.get(key):
                names[name] = key
            if names[name] == 2 or names[name] == 3:
                names[name] = "Same Name" + str(names[name])

    plt.plot(names, values, label="ID = " + str(i['ID']))


for i in range(5):
    getData(i)

plt.ylabel("Duration in minutes")
plt.xlabel("Tasks")
plt.xticks(rotation=-30)
plt.show()
