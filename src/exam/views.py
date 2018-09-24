from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from .models import Exam
from .forms import ExamForm


def home(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('exam:list')
            # Redirect to a success page.
            print('sucessfull login')
            pass
        else:
            # Return an 'invalid login' error message.
            print('unsucessfull login')
            pass
    return render(request,'base/home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

class ExamListView(ListView):
    queryset = Exam.objects.all()
    template_name = 'exam/list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExamListView, self).dispatch(*args, **kwargs)

@login_required
def CreateExamView(request,id=None):
    try:
        exam_obj = Exam.objects.get(id=id)
    except Exam.DoesNotExist:
        exam_obj = None
    print('dasdas')
    form = ExamForm(request.POST or None, instance=exam_obj)
    context = {
        'form' : form,
    }
    if request.POST:
        print('POST')
        if form.is_valid():
            print('form valid')
            exam_obj = form.save(commit=False)
            print(exam_obj.id)
            exam_obj.save()
            return redirect('exam:list')
    return render(request,'exam/create.html', context)

@login_required
def DeleteExamView(request,id):
    try:
        exam_obj = Exam.objects.get(id=id)
        exam_obj.delete()
    except Exam.DoesNotExist:
        pass
    print('successful delete')
    return redirect('exam:list')
