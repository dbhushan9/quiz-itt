from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator


from .models import Exam
from .forms import ExamForm

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
