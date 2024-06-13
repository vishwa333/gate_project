from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class subject(models.Model):
    sub_code = models.CharField(max_length = 3,primary_key=True)
    sub_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.sub_name

class chapter(models.Model):
    sub_code = models.ForeignKey(subject,default='101', on_delete=models.SET_DEFAULT)
    chap_code = models.CharField(max_length = 3,primary_key=True)
    chap_name = models.CharField(max_length=50,blank=True)
    def __str__(self):
        return self.chap_name

class topic(models.Model):
    sub_code = models.ForeignKey(chapter,default='102', on_delete=models.SET_DEFAULT)
    topic_code = models.CharField(max_length=6, primary_key=True)
    topic_name = models.CharField(max_length=50)
    def __str__(self):
        return self.topic_name
    pass

class question(models.Model):
    q_id = models.AutoField(primary_key=True,unique=True)
    q_type = models.CharField(max_length=8,choices=[('mcq', 'mcq'), ('fillin', 'fillin'), ('tf', 'tf')])
    question = models.CharField(max_length=1500)
    q_image = models.ImageField(upload_to="./qimages",blank=True)
    choice1 = models.CharField(max_length=100)
    choice2 = models.CharField(max_length=100)
    choice3 = models.CharField(max_length=100)
    choice4 = models.CharField(max_length=100)
    subject = models.ForeignKey(subject,default='101', on_delete=models.SET_DEFAULT)
    chapter = models.ForeignKey(chapter,default='102', on_delete=models.SET_DEFAULT)
    topic = models.ForeignKey(topic,default="unassigned",on_delete=models.SET_DEFAULT)
    marks = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)])
    negative = models.FloatField(choices=[(-0.33, -0.33), (0, 0), (-0.66, -0.66)])
    diff_level = models.CharField(max_length=20,choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('VeryHard', 'VeryHard')])
    attempts = models.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)
    def __str__(self):
        return self.question
    pass

class solution(models.Model):
    q_id = models.OneToOneField(question,on_delete=models.CASCADE,primary_key=True)
    answer = models.CharField(max_length=10)
    pass


