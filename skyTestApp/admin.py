from django.contrib import admin
from skyTestApp.models import Tasks

# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    list_display=['id','name','status','start_date','end_date','parent','duration','net_duration']

admin.site.register(Tasks,TasksAdmin)
