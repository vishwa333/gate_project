from django.db import models
from questions.models import *
from accounts.models import *
# Create your models here.

#class user(models.Model):
#    name = models.CharField(max_length = 100)
#    mobile = models.IntegerField()
#    email = models.CharField(max_length=30)
#    pass1 = models.CharField(max_length=10)
#    image = models.ImageField(upload_to = "staticfiles/images")

class testtype(models.Model):
    ttype = models.CharField(max_length=50)
    description = models.CharField(max_length=250,default="This is description")
    pass

class test(models.Model):
    test_id = models.AutoField(primary_key=True,unique=True)
    questions = models.ManyToManyField(question)
    test_type = models.CharField(max_length=40,default="Test",choices=[('Chapter_wise','Chapter_wise'),("Subject_wise","Subject_wise"),('Part_syllabus','Part_syllabus'),('Multi_sub','Multi_sub'),('Full_length','Full_length')])
    tsub = models.ManyToManyField(subject)
    tchap = models.ManyToManyField(chapter,blank=True)
    max_marks = models.IntegerField()
    max_time = models.IntegerField(default=10)
    difficulty = models.CharField(max_length=40,default="Easy",choices=[('Mixed','Mixed'),("Easy","Easy"),('Medium','Medium'),('Hard','Hard'),('Very_hard','Very_hard')])
    pass


class test_result(models.Model):
    test_id = models.ForeignKey(test,on_delete=models.CASCADE)
    user_id = models.ForeignKey(my_user,on_delete=models.CASCADE)
    marks = models.FloatField()

    pass

class test_responses(models.Model):
    test_id = models.ForeignKey(test, on_delete=models.CASCADE)
    question_id = models.ForeignKey(question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(my_user, on_delete=models.CASCADE)
    response = models.CharField(max_length=4)
    correctness = models.BooleanField()
    mark = models.FloatField(default=0.0)

    class Meta:
        unique_together = (("test_id", "question_id","user_id"),)
    pass

