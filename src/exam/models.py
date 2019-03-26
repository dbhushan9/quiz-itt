from datetime import date, timedelta
from .utils import unique_slug_generator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save



DEPT_CHOICES = (
    ('Computer Science', 'Computer Science'),
    ('Information Technology', 'Information Technology'),
    ('Electrical', 'Electrical'),
    ('Civil', 'Civil'),
    ('Electronics', 'Electronics')
)

def upload_image_path(instance, filename):
    return "{examid}/{id}/{file}".format(examid=instance.exam.id,id=instance.id, file=filename)

class Exam(models.Model):
    title           = models.CharField(max_length=255)
    slug            = models.SlugField(blank=True, unique=True)
    department      = models.CharField(max_length=255, choices=DEPT_CHOICES, default='Computer Science')
    exam_date       = models.DateField(default=date.today)
    start_time      = models.TimeField(default=timezone.now)
    close_time      = models.TimeField(default=timezone.now)
    duration        = models.DurationField(default=timedelta(minutes=60))
    students        = models.ManyToManyField(User, blank=True)

    def __str__(self):
            return self.title



class Question(models.Model):
    exam            = models.ForeignKey(Exam,on_delete=models.CASCADE)
    description     = models.CharField(max_length=255)
    marked          = models.BooleanField(default=False)
    image           = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    active          = models.BooleanField(default=True)

    def __str__(self):
            return self.description

class Choice(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    description     = models.CharField(max_length=255)

    def __str__(self):
            return self.description

class AnswerKey(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_key')
    choice          = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def __str__(self):
            return f"{self.question}:{self.choice}"

'''
class Instruction:
    exam            = models.ForeignKey(Exam)
    text            = models.CharField(max_length=255)

    def __str__(self):
            return self.text


'''
def exam_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(exam_pre_save_reciever, sender=Exam)
