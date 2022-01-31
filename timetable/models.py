from django.db import models


class Timetable(models.Model):
    name = models.CharField('Class Name', max_length=100)
    class_date = models.DateTimeField('Class Date')
    equipment_needed = models.CharField('Equipment Needed', max_length=100)