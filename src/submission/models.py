from django.db import models
from django.contrib.auth.models import User

from exam.models import Exam, Question, Choice, AnswerKey


class Submission(models.Model):
    exam            = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student         = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date    = models.DateField(auto_now_add=True)
    score           = models.IntegerField(default=0)

    def __str__(self):
            return f'{self.exam}:{self.student}'

class Answer(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
            return f'{self.question}:{self.selected_choice}'
