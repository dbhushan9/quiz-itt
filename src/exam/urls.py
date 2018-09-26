from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.ExamListView.as_view(),name='list' ),
    path('create/',views.CreateExamView, name='create'),
    path('edit/<int:id>', views.CreateExamView, name='edit'),
    path('delete/<int:id>', views.DeleteExamView, name='delete'),
    path('<slug:slug>/questions/', views.QuestionListView, name='question_list'),
    path('<slug:slug>/multiple_questions/', views.CreateMultipleQuestionView, name='multiple_questions'),
    path('excel/questions',views.question_excel,name='question_excel'),
    path('<slug:slug>/generate_user/',views.get_users,name='generate_user'),
]
