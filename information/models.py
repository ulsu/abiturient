# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

class SectionList(models.Model):
    title = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title
        
class SectionListAdmin(admin.ModelAdmin):
    list_display = ('title','id',)
admin.site.register(SectionList,SectionListAdmin)

class InfoList(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True,null=True)
    section = models.ForeignKey(SectionList)
    
    def __unicode__(self):
        return self.title
        
    def faculty_name(self):
        return self.section.title
        
class InfoListAdmin(admin.ModelAdmin):
    list_display = ('title','section',)
admin.site.register(InfoList,InfoListAdmin)
