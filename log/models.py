# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from form.models import Application
from datetime import datetime


class Add(models.Model):
    app = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    automech = models.BooleanField(default=False)
    datetime = models.DateTimeField(default=datetime.now())

    def name(self):
        avt_str = '(Автомех)' if self.automech else ''
        return '%s%s добавил %s %s' % (self.user.username, avt_str, self.app.id, self.datetime)

class AddAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Add,AddAdmin)