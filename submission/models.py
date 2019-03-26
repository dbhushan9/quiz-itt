from django.db import models
from django.contrib.auth.models import User

from exam.models import Exam, Question, Choice, AnswerKey

class SubmissionManager(models.Manager):
    def get_or_new(self,student,exam):
        qs = self.get_queryset().filter(student=student).filter(exam=exam)
        if qs.count() == 0:
            submission_obj = self.model.objects.create(student=student, exam=exam)
            submission_obj.save()
            new_obj = True
        else:
            submission_obj = qs.first()
            new_obj = False
        return submission_obj,new_obj

class Submission(models.Model):
    exam            = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student         = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    score           = models.IntegerField(default=0)
    finished        = models.BooleanField(default=False)

    objects         = SubmissionManager()
    def __str__(self):
            return f'{self.exam}:{self.student}'

class AnswerManager(models.Manager):
    def get_or_new(self,submission,choice,question):
        qs = self.get_queryset().filter(question=question)
        if qs.count() == 0:
            answer_obj = self.model.objects.create(submission=submission,selected_choice=choice, question=question)
            new_obj = True
        else:
            answer_obj = qs.first()
            answer_obj.selected_choice = choice
            new_obj = False
        answer_obj.save()
        return answer_obj, new_obj

class Answer(models.Model):
    submission      = models.ForeignKey(Submission, on_delete=models.CASCADE)
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    objects = AnswerManager()
    def __str__(self):
            return f'{self.question}:{self.selected_choice}'
