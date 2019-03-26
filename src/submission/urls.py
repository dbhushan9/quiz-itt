from django.urls import path

from . import views
app_name = 'submission'
urlpatterns = [
    path('exams/',views.home,name='home'),
    path('exam_instruction/<int:id>',views.exam_instruction,name='exam_instruction'),
    path('exam_attempt/',views.exam_attempt,name='attempt'),
]
