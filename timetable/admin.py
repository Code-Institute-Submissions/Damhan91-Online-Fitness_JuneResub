from django.contrib import admin
from .models import Timetable
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Timetable)
class TimtableAdmin(SummernoteModelAdmin):

    list_filter = ('name', 'class_date')
    list_display = ('name', 'class_date')
    search_fields = ['name', 'class_date']