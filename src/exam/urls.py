from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.ExamListView.as_view(),name='list' ),
    path('create/',views.CreateExamView, name='create'),
    path('edit/<int:id>', views.CreateExamView, name='edit'),
    path('delete/<int:id>', views.DeleteExamView, name='delete'),
]
