from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Submission)
admin.site.register(models.Answer)
