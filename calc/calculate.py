from .models import Course, Session
from decimal import *
# import copy

def totalUnits(session_id):
    session = Session.objects.get(sid=session_id)
    units = 0
    for course in session.course_set.all():
        units += course.units
    return units

def totalQP(session_id):
    session = Session.objects.get(sid=session_id)
    qp = 0
    for course in session.course_set.all():
        units = course.units
        if(course.grade == "A"):
            gradeMultiplier = 4
        elif(course.grade == "B"):
            gradeMultiplier = 3
        elif(course.grade == "C"):
            gradeMultiplier = 2
        elif(course.grade == "D"):
            gradeMultiplier = 1
        else:
            gradeMultiplier = 0
        course.qp = units * gradeMultiplier
        course.save()
        qp += units * gradeMultiplier
    return qp

def calculateQPA(session_id):
    units = totalUnits(session_id)
    qp = totalQP(session_id)
    return Decimal(str(qp / units)).quantize(Decimal('.01'), rounding=ROUND_DOWN)

def raiseToQPA(session_id, finalQPA):
    """
    given a qpa to reach, raises grades of all courses(or lowers them) till the 
    returned QPA is greater than the final (if it is above) or less than the final
    (if it is below.)
    """
    session = Session.objects.get(sid=session_id)
    courses = session.course_set.all()
    units = 0
    currGrades = dict()
    for course in courses:
        units += course.units
        # creates a dict with course names and their grade multipliers
        currGrades[course.courseName] = 4-(ord(course.grade)-65)
    # increases a single grade
    changedCourse = dict()
    for course in currGrades:
        if(currGrades[course]==4): #can't increase the grade if it's an A
            continue
        for i in range(4 - currGrades[course]):
            currGrades[course] += 1
            if(course not in changedCourse):
                changedCourse[course] = 0
            else:
                changedCourse[course] += 1
            if(testQPA(session_id, currGrades, finalQPA)):#currGrades, gradeList, finalQPA
                return currGrades
    for course in changedCourse:
        currGrades[course] -= changedCourse[course]
    return None

def calcDesiredQPA(session_id, gradeList, finalQPA):
    qp = 0
    units = 0
    session = Session.objects.get(sid=session_id)
    for course in session.course_set.all():
        qp += course.units * gradeList[course.courseName]
        units += course.units
    qpa = qp / units
    print("\n\nQPA:%4.2f\n\n" % qpa)
    qpa = float(Decimal(str(qpa)).quantize(Decimal("0.01")))
    return qpa

def testQPA(session_id, gradeList, finalQPA):
    qpa = calcDesiredQPA(session_id, gradeList, finalQPA)
    if(qpa >= finalQPA):
        return True
    return False
