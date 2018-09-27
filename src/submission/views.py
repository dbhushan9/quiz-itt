from django.shortcuts import render, redirect
from exam.models import Exam, Question, AnswerKey, Choice
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
import pytz
# Create your views here.


@login_required
def exam_instruction(request):
    user_obj = request.user
    try:
        exam_obj = user_obj.exam_set.all()[0]
    except:
        exam_obj = None
    return render(request,'submission/instructions.html',{'exam':exam_obj})

@login_required
def exam_attempt(request):



    user_obj = request.user
    try:
        exam_obj = user_obj.exam_set.all()[0]
    except:
        exam_obj = None

    local_dt = datetime.datetime.combine(exam_obj.exam_date,exam_obj.start_time)
    local_dt+=exam_obj.duration
    print(local_dt,local_dt.now())
    date_string = "{:%B %d, %Y %H:%M:%S}".format(local_dt)
    if request.POST:
        score =0
        for que in exam_obj.question_set.all():
            try:

                if(str(que.correct_choice.all()[0].choice.id) == str(request.POST.get(f'{que.id}'))):
                    score = score + 1
            except:
                pass
        print('score is ',score)
        return redirect('submission:exam_instruction')
    return render(request,'submission/attempt.html',{'exam':exam_obj,'date_string':date_string})
