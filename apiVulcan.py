from vulcan import Vulcan
import json
from datetime import date, timedelta, datetime



def logInVulcan(token,symbol,pin):
    certificate = Vulcan.register(token, symbol, pin)
    """with open('cert.json', 'w') as f: # You can use other filename
        json.dump(certificate.json, f)"""
    return certificate.json


"""def getCertificate():
    with open('cert.json') as f:
        certificate = json.load(f)
        return certificate"""


def getExams(date, certificate):
    client = Vulcan(certificate)
    Exams = ""
    for exam in client.get_exams(date):
        Exams += exam.teacher.first_name + " " + exam.teacher.last_name + "\n" + exam.subject.name + "\n" + exam.description + "\n" + str(exam.date) + '\n' + "\n"
    return Exams

def getHomework(date, certificate):
    client = Vulcan(certificate)
    homeworkS = ""
    for homework in client.get_homework(date):
        homeworkS += homework.teacher.first_name + " " + homework.teacher.last_name + "\n" + homework.subject.name + "\n" + "\n"
    return homeworkS

def getAverage(certificate,przedmiot):
    client = Vulcan(certificate)
    weights = 0
    grades = 0
    for grade in client.get_grades():
        if(grade.subject.name.lower()==przedmiot):
            if(len(grade.content)==2):
                if("+" in grade.content):
                    gradeG = int(grade.content[:-1])
                    gradeG += 0.25
                    grades += gradeG * int(grade.weight)
                    weights += int(grade.weight)
                else:
                    gradeG = int(grade.content[:-1])
                    gradeG -= 0.25
                    grades += gradeG * int(grade.weight)
                    weights += int(grade.weight)
            elif(grade.content.isnumeric()==True):
                grades += int(grade.content) * int(grade.weight)
                weights += int(grade.weight)
    return round(grades/weights,2)


def getStudentInfo(certificate):
    client = Vulcan(certificate)
    Info = []
    for student in client.get_students():
        Info.append(student.name)
        Info.append(str(student.class_.name))
        Info.append(str(student.school.name))
    return Info

def getMessages(certificate):
    UnreadMessages = []
    client = Vulcan(certificate)
    for message in client.get_messages():
        if(str(message.read_date)=='None'):
            UnreadMessages.append(message.sender.name)
    return UnreadMessages

def getLessons(certificate,day):
    client = Vulcan(certificate)
    LastWeek = getLastWeek()
    Lessons = []
    if(day=="pon"):
        for lesson in client.get_lessons(LastWeek[0]):
            Lessons.append(str(lesson.time.from_)[:-3]+"-"+str(lesson.time.to)[:-3])
            Lessons.append(str(lesson.subject.name))
            if(str(lesson.group)!="None"):
                Lessons.append(str(lesson.room) +" Grupa: " +str(lesson.group))
            else:
                Lessons.append(str(lesson.room))
        return Lessons
    elif(day=="wt"):
        for lesson in client.get_lessons(LastWeek[1]):
            Lessons.append(str(lesson.time.from_)[:-3]+"-"+str(lesson.time.to)[:-3])
            Lessons.append(str(lesson.subject.name))
            if(str(lesson.group)!="None"):
                Lessons.append(str(lesson.room) +" Grupa: " +str(lesson.group))
            else:
                Lessons.append(str(lesson.room))
        return Lessons
    elif(day=="sr"):
        for lesson in client.get_lessons(LastWeek[2]):
            Lessons.append(str(lesson.time.from_)[:-3]+"-"+str(lesson.time.to)[:-3])
            Lessons.append(str(lesson.subject.name))
            if(str(lesson.group)!="None"):
                Lessons.append(str(lesson.room) +" Grupa: " +str(lesson.group))
            else:
                Lessons.append(str(lesson.room))
        return Lessons
    elif(day=="czw"):
        for lesson in client.get_lessons(LastWeek[3]):
            Lessons.append(str(lesson.time.from_)[:-3]+"-"+str(lesson.time.to)[:-3])
            Lessons.append(str(lesson.subject.name))
            if(str(lesson.group)!="None"):
                Lessons.append(str(lesson.room) +" Grupa: " +str(lesson.group))
            else:
                Lessons.append(str(lesson.room))
        return Lessons
    elif(day=="pt"):
        for lesson in client.get_lessons(LastWeek[4]):
            Lessons.append(str(lesson.time.from_)[:-3]+"-"+str(lesson.time.to)[:-3])
            Lessons.append(str(lesson.subject.name))
            if(str(lesson.group)!="None"):
                Lessons.append(str(lesson.room) +" Grupa: " +str(lesson.group))
            else:
                Lessons.append(str(lesson.room))
        return Lessons


def getLastWeek():
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    WeekDays = []
    for x in range(5):
        WeekDays.append(start + timedelta(days=x))
    return WeekDays


def getLastGrade(certificate):
    client = Vulcan(certificate)
    LastGradeID = ""
    LastGradeData = ""
    returnList = []
    for grade in client.get_grades():
        LastGradeID = grade.id
        LastGradeData = grade.subject.name + "\n" + grade.content
    returnList.append(LastGradeID)
    returnList.append(LastGradeData)
    return returnList
