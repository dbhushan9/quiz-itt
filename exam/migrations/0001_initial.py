# Generated by Django 2.1.1 on 2018-09-27 14:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import exam.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('department', models.CharField(choices=[('Computer Science', 'Computer Science'), ('Information Technology', 'Information Technology'), ('Electrical', 'Electrical'), ('Civil', 'Civil'), ('Electronics', 'Electronics')], default='Computer Science', max_length=255)),
                ('exam_date', models.DateField(default=datetime.date.today)),
                ('start_time', models.TimeField(default=django.utils.timezone.now)),
                ('close_time', models.TimeField(default=django.utils.timezone.now)),
                ('duration', models.DurationField(default=datetime.timedelta(0, 3600))),
                ('students', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('marked', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=exam.models.upload_image_path)),
                ('active', models.BooleanField(default=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Exam')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Question'),
        ),
        migrations.AddField(
            model_name='answerkey',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Choice'),
        ),
        migrations.AddField(
            model_name='answerkey',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_key', to='exam.Question'),
        ),
    ]