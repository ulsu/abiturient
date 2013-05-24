# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from datetime import date

class FacultyPage(models.Model):
    title = models.CharField(max_length=255)
    introtext = models.TextField(blank=True,null=True)
    fulltext = models.TextField(blank=True,null=True)
    fulltext_en = models.TextField(blank=True,null=True)
    fulltext_de = models.TextField(blank=True,null=True)
    fotoname = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.title
        
class FacultyPageAdmin(admin.ModelAdmin):
    list_display = ('title','fotoname',)
admin.site.register(FacultyPage,FacultyPageAdmin)


class SpecPage(models.Model):
    title = models.CharField(max_length=255)
    fulltext = models.TextField(blank=True,null=True)
    faculty = models.ForeignKey(FacultyPage)
    
    def __unicode__(self):
        return self.title
        
    def faculty_name(self):
        return self.faculty.title
        
class SpecPageAdmin(admin.ModelAdmin):
    list_display = ('title','faculty_name',)
admin.site.register(SpecPage,SpecPageAdmin)

class NewsPage(models.Model):
    title = models.CharField(max_length=255)
    introtext = models.TextField(blank=True,null=True)
    fulltext = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.title
        
class NewsPageAdmin(admin.ModelAdmin):
    list_display = ('title','introtext','fulltext',)
admin.site.register(NewsPage,NewsPageAdmin)

class InfoPage(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.title
        
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(InfoPage,InfoPageAdmin)