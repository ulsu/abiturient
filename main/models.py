# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class ActivationKey(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.activation_key


class TempSpecExamRel(models.Model):
    spec = models.CharField(max_length=255)
    form = models.CharField(max_length=255)
    exam = models.CharField(max_length=255)


class ExamFull(models.Model):
    name = models.CharField(max_length=255)
    in_list = models.BooleanField(default=False)


class ExamFullAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(ExamFull, ExamFullAdmin)





class FormFull(models.Model):
    name = models.CharField(max_length=255)
    school = models.BooleanField(default=False)


class FormFullAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(FormFull, FormFullAdmin)


class SpecExam(models.Model):
    spec = models.ForeignKey('SpecFull')
    form = models.ForeignKey(FormFull)
    exam = models.ForeignKey(ExamFull)


class SpecExamAdmin(admin.ModelAdmin):
    list_display = ('spec', 'form', 'exam',)
admin.site.register(SpecExam, SpecExamAdmin)


class SpecFull(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class SpecFullAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(SpecFull, SpecFullAdmin)