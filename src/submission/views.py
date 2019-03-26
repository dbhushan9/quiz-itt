from django.shortcuts import render, redirect
from django.http import HttpResponse
from exam.models import Exam, Question, AnswerKey, Choice
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
import pytz
import random

from .models import Submission, Answer


@login_required
def exam_instruction(request,id):
    user_obj = request.user
    try:
        exam_obj = Exam.objects.get(id=id)
        print("users: ",exam_obj.students.all());
        if user_obj not in exam_obj.students.all():
            exam_obj.students.add(user_obj)
    except:
        redirect('submission:home')
    return render(request,'submission/instructions.html',{'exam':exam_obj})

@login_required
def home(request):
    exam_list = Exam.objects.all()
    context = {'exam_list':exam_list};
    return render(request,'submission/exam_list.html', context)




@login_required
def exam_attempt(request):
    user_obj = request.user
    try:
        exam_obj = user_obj.exam_set.all().first()
        submission_obj,new_obj = Submission.objects.get_or_new(student=user_obj,exam=exam_obj)
        print(submission_obj, new_obj)
    except Exception as e:
        return HttpResponse('<h1>No Exam exists for this User contact Administrator</h1>')

    if request.POST:
        score =0
        for que in exam_obj.question_set.all():
            try:
                choice_id = str(request.POST.get(f'{que.id}'))
                choice_obj = Choice.objects.get(id=choice_id)
                answer_obj,new_obj = Answer.objects.get_or_new(submission=submission_obj,choice=choice_obj, question=que)
                if(que.answer_key.all().first().choice == choice_obj ):
                    score = score + 1

            except Exception as e:
                ''' requested radio button has nothing selected  '''
                pass

        submission_obj.score = score;
        #submission_obj.finished = True;
        submission_obj.save()
        return HttpResponse(f'<h1>Your Attempt has Finished.Score {score}</h1>')
        #return redirect('submission:exam_instruction')

    deadline = submission_obj.created_at + exam_obj.duration
    date_string = "{:%B %d, %Y %H:%M:%S}".format(deadline)

    if submission_obj.finished :
        return HttpResponse('<h1>Your Attempt has Finished</h1>')
    if deadline <= timezone.now() or submission_obj.finished :
        #submission_obj.finished = True
        #submission_obj.save()
        return HttpResponse('<h1>Exam Finished</h1>')

    question_set = exam_obj.question_set.all()
    question_set=list(question_set)
    random.shuffle(question_set)
    print(question_set)
    print("TESTING !@# +++++++++++++++++++++++++++++++++++++++++++++++")
    return render(request,'submission/attempt.html',{'exam':exam_obj,'questions':question_set,'date_string':date_string,'submission':submission_obj})
