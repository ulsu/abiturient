# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User




#Cловари для формы

class IDSocialStatus(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class IDSocialStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(IDSocialStatus,IDSocialStatusAdmin)


class Nationality(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class NationalityAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Nationality,NationalityAdmin)


class MilitaryStatus(models.Model):
    name=models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class MilitaryStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(MilitaryStatus,MilitaryStatusAdmin)


class Language(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Language,LanguageAdmin)


class Privilege(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Privilege,PrivilegeAdmin)


class Diplom(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class DiplomAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Diplom,DiplomAdmin)


class EduType(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class EduTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EduType,EduTypeAdmin)


class ExamName(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class ExamNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(ExamName,ExamNameAdmin)


class ULSUCource(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class ULSUCourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(ULSUCource,ULSUCourceAdmin)


class InstituteType(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class InstituteTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(InstituteType,InstituteTypeAdmin)











class EduRegion(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class EduRegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EduRegion,EduRegionAdmin)




class EduLocality(models.Model):
    name   = models.CharField(max_length=255)
    region = models.ForeignKey(EduRegion)
    def __unicode__(self):
        return self.name

class EduLocalityAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EduLocality,EduLocalityAdmin)




class EduInstitute(models.Model):
    name  = models.CharField(max_length=255)
    local = models.ForeignKey(EduLocality)
    type  = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class EduInstituteAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EduInstitute,EduInstituteAdmin)



















class Country(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Country,CountryAdmin)


class Region(models.Model):
    name   = models.CharField(max_length=255)
    type   = models.CharField(max_length=255)
    index  = models.IntegerField()
    gninmb = models.IntegerField()
    uno    = models.IntegerField()
    ocatd  = models.IntegerField()
    status = models.IntegerField()
    def __unicode__(self):
        return self.name

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name','type','gninmb','index')
admin.site.register(Region,RegionAdmin)




class RegionArea(models.Model):
    area_id = models.IntegerField()
    region  = models.ForeignKey(Region)
    old_id  = models.IntegerField()
    name    = models.CharField(max_length=255)
    type    = models.CharField(max_length=255)
    code    = models.IntegerField()
    index   = models.IntegerField()
    gninmb  = models.IntegerField()
    uno     = models.IntegerField()
    ocatd   = models.IntegerField()
    status  = models.IntegerField()
    def __unicode__(self):
        return self.name

class RegionAreaAdmin(admin.ModelAdmin):
    list_display = ('name','type','gninmb','index')
admin.site.register(RegionArea,RegionAreaAdmin)



class Locality(models.Model):
    city_id = models.IntegerField()
    area_id = models.IntegerField()
    region  = models.ForeignKey(Region)
    name    = models.CharField(max_length=255)
    type    = models.CharField(max_length=255)
    code    = models.IntegerField()
    index   = models.IntegerField()
    gninmb  = models.IntegerField()
    uno     = models.IntegerField()
    ocatd   = models.IntegerField()
    status  = models.IntegerField()
    def __unicode__(self):
        return self.name

class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name','type','gninmb','index')
admin.site.register(Locality,LocalityAdmin)



class Street(models.Model):
    street_id = models.IntegerField()
    city_id = models.IntegerField()
    area_id = models.IntegerField()
    region  = models.ForeignKey(Region)
    name    = models.CharField(max_length=255)
    type    = models.CharField(max_length=255)
    code    = models.BigIntegerField()
    index   = models.IntegerField()
    gninmb  = models.IntegerField()
    uno     = models.IntegerField()
    ocatd   = models.IntegerField()
    def __unicode__(self):
        return self.name

class StreetAdmin(admin.ModelAdmin):
    list_display = ('name','type','gninmb','index')
admin.site.register(Street,StreetAdmin)









class Speciality(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Speciality,SpecialityAdmin)





class SpecialityFaculty(models.Model):
    speciality = models.ForeignKey('Speciality')
    faculty = models.ForeignKey('Faculty')
    description = models.TextField()
    def name(self):
        return self.faculty.name + ' ' + self.speciality.name
    def __unicode__(self):
        return self.name()

class SpecialityFacultyAdmin(admin.ModelAdmin):
    list_display = ('speciality','faculty',)
admin.site.register(SpecialityFaculty,SpecialityFacultyAdmin)


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    introtext = models.TextField()
    fulltext = models.TextField()
    fulltext_en = models.TextField(blank=True,null=True)
    fulltext_de = models.TextField(blank=True,null=True)
    photo = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def specialities(self):
        return SpecialityFaculty.objects.filter(faculty=self)

    def en(self):
            return 'Есть' if self.fulltext_en else ''

    def de(self):
        return 'Есть' if self.fulltext_de else ''

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name','photo','en','de',)
admin.site.register(Faculty,FacultyAdmin)


class EduForm(models.Model):
    name = models.CharField(max_length=255)
    school = models.BooleanField()
    spo = models.BooleanField()
    def __unicode__(self):
        return self.name

class EduFormAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EduForm,EduFormAdmin)


class MainSpec(models.Model):
    speciality_faculty = models.ForeignKey(SpecialityFaculty)
    mainspec_id = models.IntegerField()
    edu_form = models.ForeignKey(EduForm)
    exams = models.ManyToManyField('ExamSpec')
    def __unicode__(self):
        return self.speciality_faculty.name() + ' ' + self.edu_form.name

class MainSpecAdmin(admin.ModelAdmin):
    list_display = ('mainspec_id', 'speciality_faculty', 'edu_form',)
admin.site.register(MainSpec,MainSpecAdmin)


class ExamSpec(models.Model):
    name = models.CharField(max_length=255)
    in_list = models.BooleanField()
    def __unicode__(self):
        return self.name

class ExamSpecAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(ExamSpec,ExamSpecAdmin)




class Fach(models.Model):
    STREAM=(
        (1,'Первый поток'),
    )
    speciality = models.ForeignKey(Speciality,   blank=True, null = True)
    faculty    = models.ForeignKey(Faculty,      blank=True, null = True)
    edu_form   = models.ManyToManyField(EduForm, blank=True, null = True)
    Priority   = models.IntegerField(1,          blank=True, null = True)
    Stream     = models.IntegerField(            blank=True, null = True, choices=STREAM)
    Service    = models.IntegerField(            blank=True, null = True)
    user       = models.ForeignKey(User)


    def edu_forms(self):
        if not self.speciality or not self.faculty: return []
        specfac = SpecialityFaculty.objects.filter(speciality=self.speciality, faculty=self.faculty)
        edu_forms = []
        for e in MainSpec.objects.filter(speciality_faculty=specfac):
            edu_forms.append(e.edu_form.id)
        return edu_forms

    def edu_form_names(self):
        if not self.speciality or not self.faculty: return []
        specfac = SpecialityFaculty.objects.filter(speciality=self.speciality, faculty=self.faculty)
        edu_forms = ''
        for e in MainSpec.objects.filter(speciality_faculty=specfac):
            edu_forms += ' ' + e.edu_form.name
        return edu_forms

    def active_edu_forms(self):
        ids = []
        for e in self.edu_form.all():
            ids.append(e.id)
        return ids

    def facs(self):
        if not self.speciality: return []
        facs = SpecialityFaculty.objects.filter(speciality=self.speciality)
        ids = []
        for f in facs:
            ids.append(f.faculty.id)
        return ids


class FachAdmin(admin.ModelAdmin):
    list_display = ('speciality','faculty','edu_form_names','Priority','Stream','Service',)
admin.site.register(Fach,FachAdmin)















class Exam(models.Model):
    Number   = models.CharField(max_length=20,  blank=True)
    ExamName = models.ForeignKey(ExamName,      blank=True, null = True)
    Mark     = models.IntegerField(             blank=True, null = True)
    DocSer   = models.IntegerField(4,           blank=True, null = True)
    DocNum   = models.IntegerField(6,           blank=True, null = True)
    user     = models.ForeignKey(User)

class ExamAdmin(admin.ModelAdmin):
    list_display = ('Number','ExamName','Mark','user',)
admin.site.register(Exam,ExamAdmin)








class Application(models.Model):
    GENDER=(
        (1,'Male'),
        (2,'Female'),
    )

    user            = models.OneToOneField(User)
    FirstName       = models.CharField(max_length=255,  blank=True)
    LastName        = models.CharField(max_length=255,  blank=True)
    MiddleName      = models.CharField(max_length=255,  blank=True)
    BirthDay        = models.DateField(                 blank=True, null = True)
    IDSex           = models.IntegerField(              blank=True, null = True, choices=GENDER)
    IDSocialStatus  = models.ForeignKey(IDSocialStatus, blank=True, null = True)
    Nationality     = models.ForeignKey(Nationality,    blank=True, null = True)
    Citizenship     = models.ForeignKey(Country,        blank=True, null = True, related_name='+')

    PassportSer     = models.IntegerField(max_length=4, blank=True, null = True)
    PassportNumb    = models.IntegerField(max_length=6, blank=True, null = True)
    CodUVD          = models.CharField(max_length=7,    blank=True, null = True)
    PassportDate    = models.DateField(                 blank=True, null = True)
    BirthPlace      = models.CharField(max_length=255,  blank=True)
    PassportIssued  = models.CharField(max_length=255,  blank=True)

    PrCountry       = models.ForeignKey(Country,    related_name='+', blank=True, null = True)
    PrRegion        = models.ForeignKey(Region,     related_name='+', blank=True, null = True)
    PrRegionArea    = models.ForeignKey(RegionArea, related_name='+', blank=True, null = True)
    PrLocality      = models.ForeignKey(Locality,   related_name='+', blank=True, null = True)
    PrStreet        = models.ForeignKey(Street,     related_name='+', blank=True, null = True)
    PrHouse         = models.CharField(max_length=255,  blank=True)
    PrApartment     = models.CharField(max_length=255,  blank=True)
    PrIndex         = models.IntegerField(max_length=6, blank=True, null = True)
    Telephone       = models.CharField(max_length=255,  blank=True)
    Email           = models.CharField(max_length=255,  blank=True)
    prp             = models.BooleanField(default = True)
    
    LiveCountry     = models.ForeignKey(Country,    related_name='+', blank=True, null = True)
    LiveRegion      = models.ForeignKey(Region,     related_name='+', blank=True, null = True)
    LiveRegionArea  = models.ForeignKey(RegionArea, related_name='+', blank=True, null = True)
    LiveLocality    = models.ForeignKey(Locality,   related_name='+', blank=True, null = True)
    LiveStreet      = models.ForeignKey(Street,     related_name='+', blank=True, null = True)
    LiveHouse       = models.CharField(max_length=255, blank=True)
    LiveApartment   = models.CharField(max_length=255, blank=True)
    LiveIndex       = models.IntegerField(max_length=6, blank=True, null = True)

    Hostel              = models.BooleanField()
    ForeignLanguage     = models.ForeignKey(Language,       blank=True, null = True)
    LengthServiceTotal  = models.IntegerField(              blank=True, null = True)
    PrivIDPrivileges    = models.ForeignKey(Privilege,      blank=True, null = True)
    IDMilitaryService   = models.ForeignKey(MilitaryStatus, blank=True, null = True)

    schoolRjn       = models.ForeignKey(EduRegion,    blank=True, null = True)
    schoolCity      = models.ForeignKey(EduLocality,  blank=True, null = True)
    schoolName      = models.ForeignKey(EduInstitute, blank=True, null = True)
    schoolSel       = models.BooleanField(default = False)

    EduCountry              = models.ForeignKey(Country,   related_name='+', blank=True, null = True)
    EduRegion               = models.ForeignKey(Region,    related_name='+', blank=True, null = True)
    EduRegionArea           = models.ForeignKey(RegionArea,related_name='+', blank=True, null = True)
    EduLocality             = models.ForeignKey(Locality,  related_name='+', blank=True, null = True)
    EduInstituteType        = models.ForeignKey(InstituteType, blank=True, null = True)
    EduInstituteName        = models.CharField(max_length=255, blank=True)
    EduInstituteDescription = models.CharField(max_length=255, blank=True)

    EduDiplomType       = models.ForeignKey(Diplom,  blank=True, null = True)
    EduEducationType    = models.ForeignKey(EduType, blank=True, null = True)
    EduDateIN           = models.DateField(blank=True, null = True)
    EduDateOUT          = models.DateField(blank=True, null = True)
    EduDiplomspeciality = models.CharField(max_length=255, blank=True)
    EduSeriaDiplom      = models.CharField(max_length=255, blank=True)
    EduNumberDiplom     = models.CharField(max_length=255, blank=True)

    UlsuIDStructure = models.ForeignKey(ULSUCource, blank=True, null = True)
    UlsuDateIn      = models.DateField(blank=True, null = True)
    UlsuDateOut     = models.DateField(blank=True, null = True)
    Original        = models.BooleanField(default = False)

    Approved = models.BooleanField(default=False)
    approve_date = models.DateTimeField(blank=True, null = True)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user','FirstName','MiddleName','LastName')

admin.site.register(Application,ApplicationAdmin)





