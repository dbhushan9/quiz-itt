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
def exam_attempt(request,id):
    user_obj = request.user
    try:
        exam_obj = Exam.objects.get(id=id) 
        exam_close_date_time = datetime.datetime.combine(exam_obj.exam_date,exam_obj.close_time)
        exam_start_date_time = datetime.datetime.combine(exam_obj.exam_date,exam_obj.start_time)
        now_date_time = timezone.now()
        # exam_close_date_time = pytz,localize(exam_close_date_time) 
        print(exam_start_date_time)
        print(now_date_time)
        print(exam_close_date_time)
        if(now_date_time < exam_start_date_time):
            return render(request,'submission/error.html',{'error':'You are Early to the Party'}) 
        
        if(now_date_time > exam_close_date_time):
            return render(request,'submission/error.html',{'error':'You are Late to the Party'}) 
        
        submission_obj,new_obj = Submission.objects.get_or_new(student=user_obj,exam=exam_obj)
        
    except Exception as e:
        print(e)
        return render(request,'submission/error.html',{'error':'Your Attempt has finished'})
   
    if request.POST:
        score =0
        print(request.POST)
        for que in exam_obj.question_set.all():
            print("trying....\n")
            try:
                choice_id = str(request.POST.get(f'{que.id}'))
                choice_obj = Choice.objects.get(id=choice_id)
                answer_obj,new_obj = Answer.objects.get_or_new(submission=submission_obj,choice=choice_obj, question=que)
                print("------",que.answer_key.all().first().choice , choice_obj )
                if(que.answer_key.all().first().choice == choice_obj ):
                    score = score + 1

            except Exception as e:
                ''' requested radio button has nothing selected  '''
                print(e)

        submission_obj.score = score;
        submission_obj.finished = True;
        submission_obj.save()
        return render(request,'submission/score.html',{'exam':exam_obj,'score':score})
        #return redirect('submission:exam_instruction')


    deadline = submission_obj.created_at + exam_obj.duration
    date_string = "{:%B %d, %Y %H:%M:%S}".format(deadline)

    if submission_obj.finished :
        return render(request,'submission/error.html',{'error':'Your Attempt has finished'})
    print('current: ',timezone.now())
    print('deadline',deadline)
    if deadline <= timezone.now() or submission_obj.finished :
        submission_obj.finished = True
        submission_obj.save()
        return render(request,'submission/error.html',{'error':'Exam has finished'})

    #question_set = exam_obj.question_set.all()
    #question_set=list(question_set)
    #random.shuffle(question_set)
    #print(question_set)
    #print("TESTING !@# +++++++++++++++++++++++++++++++++++++++++++++++")
    return render(request,'submission/attempt.html',{'exam':exam_obj,'date_string':date_string,'submission':submission_obj})
