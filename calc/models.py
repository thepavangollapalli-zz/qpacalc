from django.db import models

class Session(models.Model):
    sid = models.CharField(max_length=300)

    def __str__(self):
        return self.sid

# Create your models here.
class Course(models.Model):
    session = models.ForeignKey(Session, on_delete = models.CASCADE)
    courseName = models.CharField(max_length = 10)
    units = models.IntegerField()
    grade = models.CharField(max_length = 3)
    qp = models.IntegerField()

    def __str__(self):
        return self.courseName