from django import forms
from .models import Exam

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title','department','exam_date','start_time', 'close_time', 'duration']
        widgets = {'exam_date':DateInput(),'start_time':TimeInput(),'close_time':TimeInput()}
