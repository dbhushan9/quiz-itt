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

def exam_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(exam_pre_save_reciever, sender=Exam)



'''
class Instruction:
    exam            = models.ForeignKey(Exam)
    text            = models.CharField(max_length=255)

    def __str__(self):
            return self.text


class Question:
    exam            = models.ForeignKey(Exam)
    description     = models.CharField(max_length=255)
    marked          = models.BooleanField(default=False)
    image           = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    correct         = models.ForeignKey(Choice)
    active          = models.BooleanField(default=True)

    def __str__(self):
            return self.text


class Choice:
    question        = models.ForeignKey(Question)
    description     = models.CharField(max_length=255)

    def __str__(self):
            return self.description


class Submission:
    score
    answer - many answers to one submission
    def __str__(self):
            return self.text


class Answer:
    question
    Choice
'''
