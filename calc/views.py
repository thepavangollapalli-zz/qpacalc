from django.shortcuts import render
from .models import Session, Course
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .calculate import *

calculatedTargetQPA = 0
newGradeList = []
desiredQPA = 0
session = None
session_id = None

# Create your views here.
def index(request):
    global calculatedTargetQPA
    global newGradeList
    global desiredQPA
    global session
    global session_id
    request.session.save()
    (units, totalqp, qpa) = (0,0,0)
    if not request.session.exists(request.session.session_key):
        request.session.create()
    if(not Session.objects.filter(sid=request.session.session_key).exists()):
        session = Session(sid=request.session.session_key)
        print("\n\nNEW SESSION", request.session.session_key)
        session.save()
    else:
        print("\n\nSESSION EXISTS", Session.objects.get(sid=request.session.session_key))
        session = Session.objects.get(sid=request.session.session_key)
    if(request.session.session_key != session_id):
        print("\n\n***SESSION WILL BE CHANGED***")
        print("previous session: ",session_id)
        print("next session:", request.session.session_key)
    session_id = request.session.session_key
    courses = session.course_set.all()
    if(len(courses) > 0):
        units = totalUnits(session_id)
        totalqp = totalQP(session_id)
        qpa = calculateQPA(session_id)
    resultsDict = {"units": units, "totalqp": totalqp, "qpa": qpa}
    if(desiredQPA > 0):
        resultsDict["desiredQPA"] = desiredQPA
    if(calculatedTargetQPA > 0):
        resultsDict["calculatedTargetQPA"] = calculatedTargetQPA
    if(len(newGradeList) > 0):
        resultsDict["passingGradeList"] = formatNewGrades(newGradeList)
    context = {"courses": courses, "results": resultsDict}
    calculatedTargetQPA = 0
    newGradeList = []
    desiredQPA = 0
    return render(request, "calc/index.html", context)

class AddView(generic.View):
    def get(self, request):
        global session_id
        session_id = request.session.session_key
        return render(request, "calc/add.html", {"what":None})

    def post(self, request):
        global session
        global session_id
        grade = request.POST["grade"]
        units = request.POST["units"]
        course = request.POST["course"]
        session.course_set.create(courseName = course, units = units, grade = grade, qp=0)
        totalQP(session_id)
        # newCourse = Course(courseName = course, units = units, grade = grade, qp=0)
        # newCourse.save()`
        return HttpResponseRedirect(reverse('calc:index'))

class CalcView(generic.View):
    def get(self, request):
        return render(request, 'calc/calc.html')

    def post(self, request):
        global calculatedTargetQPA
        global newGradeList
        global desiredQPA
        session_id = request.session.session_key
        desiredQPA = float(request.POST["qpa"])
        newGradeList = raiseToQPA(session_id, desiredQPA)
        calculatedTargetQPA = calcDesiredQPA(session_id, newGradeList, desiredQPA)
        return HttpResponseRedirect(reverse('calc:index'))

def formatNewGrades(gradeList):
    for course in gradeList:
        if(isinstance(gradeList[course], int)):
            gradeList[course] = chr(abs(gradeList[course]-4)+65)
    return gradeList