# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import loader, Context, RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from log.models import Add
from models import *
from django import forms
from django.http import Http404
import json
from itertools import count, izip
from datetime import datetime
import time
import pyodbc

@login_required
def main(request):
    if request.user.groups.filter(name='Publisher'):
        return show_list(request)
    else:
        is_created = Application.objects.filter(user=request.user)
        if is_created:
            a = is_created[0]
        else:
            a = Application()
            a.user = request.user
            a.save()
        return show_form(request, a)

@login_required
def add(request):
    if request.user.groups.filter(name='Publisher'):
        user = temp_user()
        try:
            a = Application.objects.get(user = temp_user())
            a.delete()
        except:
            pass
        a = Application()
        a.user = user
        a.save()
        return show_form(request, a, True)
    else:
        raise Http404


def min_array(a):
    c = None
    for i in range(len(a)):
        if a[i]!='':
            c = i
            break
    if c is None:
        return None
    else:
        m = a[c]
        for i in range(len(a)):
            if a[i] == '':
                continue
            else:
                if a[i]<m:
                    m = a[i]
                    c = i
        return c

def max_array(a):
    c = None
    for i in range(len(a)):
        if a[i]!='':
            c = i
            break
    if c is None:
        return None
    else:
        m = a[c]
        for i in range(len(a)):
            if a[i] == '':
                continue
            else:
                if a[i]>m:
                    m = a[i]
                    c = i
        return c

def real_ranges(a,plus=0):
    if a == []:
        return a
    if len(a) == max(a):
        return a
    else:
        for i in range(len(a)):
            a[i] = int(a[i]) if a[i]!='' else ''
        n = a[max_array(a)]+1
        l = 1
        b = ['' for x in range(len(a))]
        for i in range(len(a)):
            m = min_array(a)
            if m is None or a[m] == n:
                return b
            b[m] = l
            l += 1
            a[m] = n
        for i in range(len(b)):
            if b[i]!='':
                b[i] += plus
        return b

@login_required
def show_form(request, a, add=False):

    is_publisher  = request.user.groups.filter(name='Publisher')

    edit = False
    if a.Approved:
        edit = True

    t = loader.get_template("form.html")
    c = RequestContext(request, {
        'IDSocialStatus': IDSocialStatus.objects.all(),
        'Nationality':    Nationality.objects.all(),
        'Country':        Country.objects.all(),
        'Region':         Region.objects.all(),
        'RegionArea':     RegionArea.objects.all(),
        'MilitaryStatus': MilitaryStatus.objects.all(),
        'Language':       Language.objects.all(),
        'Privilege':      Privilege.objects.all(),
        'EduRegion':      EduRegion.objects.all(),
        'EduLocality':    EduLocality.objects.filter(region=a.schoolRjn) if a.schoolRjn else [],
        'EduInstitute':   EduInstitute.objects.filter(local=a.schoolCity) if a.schoolCity else [],
        'InstituteType':  InstituteType.objects.all(),
        'DiplomType':     Diplom.objects.all(),
        'EducationType':  EduType.objects.all(),
        'ExamName':       ExamName.objects.all(),
        'Speciality':     Speciality.objects.all().order_by('name'),
        'SpecialityName': Speciality.objects.all().order_by('name'),
        'EduForm':        EduForm.objects.all(),
        'Faculty':        Faculty.objects.all(),
        'Course':         ULSUCource.objects.all(),
        'v': a,
        'e': Exam.objects.filter(user = a.user),
        'f': Fach.objects.filter(user = a.user),
        'add': add,
        'publisher': is_publisher,
        'edit': edit,
        })
    return HttpResponse(t.render(c))


def get_data(request):
    if request.GET['task'] == 'loadregionareas':
        items = RegionArea.objects.filter(
            region_id = request.GET['regionid']
        )

        term = []
        for item in items:
            term.append({'id': item.id, 'name': item.name})
        return HttpResponse(json.dumps(term))

    if request.GET['task'] == 'loadlocalities':
        area_id = RegionArea.objects.get(id=int(request.GET['areaid'])).area_id if int(request.GET['areaid']) != 0 else 0
        items = Locality.objects.filter(
            region_id=Region.objects.get(id=request.GET['regionid']),
            area_id=area_id,
            name__istartswith=request.GET['term']
        )

        term = []
        term_names = []
        term_doubles = []
        for item in items:
            label = item.type + '. ' + item.name
            term.append({'id': item.id, 'name': item.name, 'label': label})
            if label not in term_names:
                term_names.append(label)
            else:
                term_doubles.append(label)

        if term_doubles:
            for item in term:
                if item['label'] in term_doubles:

                    area = Locality.objects.get( id = int(item['id']) ).area_id
                    if area == 0:
                        continue
                    else:
                        area_item = RegionArea.objects.get( area_id = area, region_id = request.GET['regionid'])
                        item['label'] += ' (' + area_item.name + ' ' + area_item.type + ')'
                        item['name'] += ' (' + area_item.name + ' ' + area_item.type + ')'

        return HttpResponse(json.dumps(term))


    if request.GET['task'] == 'loadstreets':
        items = Street.objects.filter(
            region_id=Region.objects.get(id = request.GET['regionid']),
            area_id=Locality.objects.get(id = request.GET['localid']).area_id,
            city_id=Locality.objects.get(id = request.GET['localid']).city_id,
            name__istartswith = request.GET['term']
        )

        term = []
        for item in items:
            term.append({
                'id': item.id,
                'name': item.name,
                'label': item.type + '. ' + item.name,
                'index': item.index
            })

        return HttpResponse(json.dumps(term))


    elif request.GET['task'] == 'loadedulocalities':
        localities = EduLocality.objects.filter(region = EduRegion.objects.get(id = request.GET['regionid']))
        term_local=[]
        for l in localities:
            term_local.append({'id':l.id, 'name':l.name})
        return HttpResponse(json.dumps(term_local))


    elif request.GET['task'] == 'loadeduinstitutes':
        institutes = EduInstitute.objects.filter(local = EduLocality.objects.get(id = request.GET['localid']))
        term_inst=[]
        for i in institutes:
            term_inst.append({'id':i.id, 'name':i.name})
        return HttpResponse(json.dumps(term_inst))


    elif request.GET['task'] == 'loadfacs':
        spec = Speciality.objects.get(id=request.GET['specid'])
        specfacs = SpecialityFaculty.objects.filter(speciality = spec)
        facs = []
        for s in specfacs:
            facs.append({'id': s.faculty.id, 'name':s.faculty.name})
        return HttpResponse(json.dumps(facs))


    elif request.GET['task'] == 'loadeduforms':
        specfac = SpecialityFaculty.objects.get(speciality_id=request.GET['specid'], faculty_id=request.GET['facid'])
        edu_forms = MainSpec.objects.filter(speciality_faculty = specfac)

        ids = []
        spo = int(request.GET['onlyspo'])==1
        school = int(request.GET['school'])==1
        for e in edu_forms:
            if (not spo or e.edu_form.id in [1, 2]) and (not school or not e.edu_form.id in [5, 6, 7, 17, 18, 19]):
                ids.append(e.edu_form.id)
        return HttpResponse(json.dumps(ids))

    else:
        raise Http404


def generator(req):
    pass


def safe(request, key, blank = False):
    try:
        i = request.POST[key]
    except:
        if blank:
            return ''
        else:
            return None
    else:
        if i:
            return i
        else:
            if blank:
                return ''
            else:
                return None


def safe_int(request, c, key):
    try:
        obj = c.objects.get(id=int(request.POST[key]))
    except:
        return None
    else:
        return obj


def temp_user():
    try:
        user = User.objects.get(username='temp_user')
    except:
        user = User()
        user.username = 'temp_user'
        user.set_unusable_password()
        user.save()
    return user



def valid_date(date):
    try:
        b = time.strptime(date, '%Y-%m-%d')
    except:
        return None

    if b.tm_year > datetime.now().year - 100:
         return date


def do_save(request, a):
    a.FirstName  = request.POST['FirstName']
    a.MiddleName = request.POST['MiddleName']
    a.LastName   = request.POST['LastName']

    a.BirthDay = valid_date(request.POST['BirthDay']) if request.POST['BirthDay'] else None

    a.IDSex = safe(request, 'IDSex')

    a.IDSocialStatus = safe_int(request, IDSocialStatus, 'IDSocialStatus')
    a.Nationality    = safe_int(request, Nationality, 'Nationality')
    a.Citizenship    = safe_int(request, Country, 'Citizenship')

    a.PassportSer    = safe(request, 'PassportSer')
    a.PassportNumb   = safe(request, 'PassportNumb')
    a.CodUVD         = safe(request, 'CodUVD')
    a.PassportDate   = valid_date(request.POST['PassportDate']) if request.POST['PassportDate'] else None

    a.BirthPlace     = safe(request, 'BirthPlace', True)
    a.PassportIssued = safe(request, 'PassportIssued', True)


    Russia = Country.objects.get(id=10)

    #Сохранение адреса проживания
    #TODO: запилить проверки на соответствие (такая улица есть в таком городе и т.д.)
    PrCountry = safe_int(request, Country, 'Country')
    PrRegion = safe_int(request, Region, 'Region')
    PrRegionArea = safe_int(request, RegionArea, 'RegionArea')
    PrLocality = safe_int(request, Locality, 'Locality')
    PrStreet = safe_int(request, Street, 'Street')

    PrHouse = safe(request, 'House', True)
    PrApartment = safe(request, 'Apartment', True)


    a.PrCountry = PrCountry
    if not PrCountry is None and PrCountry == Russia:
        a.PrRegion = PrRegion

        if not PrRegion is None:
            a.PrRegionArea = PrRegionArea
            a.PrLocality = PrLocality

            if not PrLocality is None:
                a.PrStreet = PrStreet

                if not PrStreet is None:
                    a.PrHouse = PrHouse
                    a.PrApartment = PrApartment
                else:
                    a.PrHouse = ''
                    a.PrApartment = ''
            else:
                a.PrHouse = ''
                a.PrApartment = ''
                a.PrStreet = None

        else:
            a.PrHouse = ''
            a.PrApartment = ''
            a.PrRegionArea = None
            a.PrLocality = None
            a.PrStreet = None

    else:
        a.PrHouse = ''
        a.PrApartment = ''
        a.PrRegion = None
        a.PrRegionArea = None
        a.PrLocality = None
        a.PrStreet = None

    a.PrIndex = safe(request, 'Index')

    a.Telephone = safe(request, 'Telephone', True)
    a.Email = safe(request, 'Email', True)
    a.IDMilitaryService = safe_int(request, MilitaryStatus, 'IDMilitaryService')

    if not 'prp' in request.POST:
        a.prp = False
        a.LiveStreet = Street.objects.get(id = int(request.POST['LiveStreet'])) if request.POST['LiveStreet'] else None
        a.LiveHouse     = request.POST['LiveHouse']     if 'LiveHouse' in request.POST     else ''
        a.LiveApartment = request.POST['LiveApartment'] if 'LiveApartment' in request.POST else ''
        a.LiveIndex     = request.POST['LiveIndex']     if request.POST['LiveIndex']       else None
    else:
        a.prp = True
        a.LiveStreet    = None
        a.LiveHouse     = ''
        a.LiveApartment = ''
        a.LiveIndex     = None


    a.Hostel             = True if 'Hostel' in request.POST else False
    a.ForeignLanguage    = Language.objects.get(id = int(request.POST['ForeignLanguage'])) if request.POST['ForeignLanguage'] else None
    a.LengthServiceTotal = request.POST['LengthServiceTotal'] if request.POST['LengthServiceTotal'] else None
    a.PrivIDPrivileges   = Privilege.objects.get(id = int(request.POST['PrivIDPrivileges'])) if request.POST['PrivIDPrivileges'] else None

    if not 'schoolSel' in request.POST:
        a.schoolSel  = False
        a.schoolRjn  = Region.objects.get(id = int(request.POST['schoolRjn']) )        if request.POST['schoolRjn'] else None
        a.schoolCity = Locality.objects.get(id = int(request.POST['schoolCity']) )  if request.POST['schoolRjn'] and request.POST['schoolCity'] else None
        a.schoolName = EduInstitute.objects.get(id = int(request.POST['schoolName']) ) if request.POST['schoolRjn'] and request.POST['schoolCity'] and request.POST['schoolName'] else None

        a.EduRegion        = None
        a.EduLocality      = None
        a.EduInstituteType = None
        a.EduInstituteName = ''
        a.EduInstituteDescription = ''
    else:
        a.schoolSel = True
        a.schoolRjn = None
        a.schoolCity = None
        a.schoolName = None



        EduCountry = safe_int(request, Country, 'EduCountry')
        EduRegion  = safe_int(request, Region, 'EduRegion')
        EduLocality = safe_int(request, Locality,'EduLocality')
        EduInstituteType = safe_int(request, InstituteType, 'EduInstituteType')

        a.EduCountry = EduCountry
        if EduCountry is None or EduCountry != 10:
            a.EduRegion = None
            a.EduLocality = None
            a.EduInstituteType = None
            a.EduInstituteName = ''
            a.EduInstituteDescription = ''
        else:
            a.EduRegion = EduRegion
            if EduRegion is None:
                a.EduLocality = None
                a.EduInstituteType = None
                a.EduInstituteName = ''
                a.EduInstituteDescription = ''
            else:
                a.EduLocality = EduLocality
                if EduLocality is None:
                    a.EduInstituteType = None
                    a.EduInstituteName = ''
                    a.EduInstituteDescription = ''
                else:
                    a.EduInstituteType = EduInstituteType
                    a.EduInstituteName = safe(request.POST['EduInstituteName'])
                    a.EduInstituteDescription = safe(request.POST['EduInstituteDescription'])


    a.EduDiplomType    = Diplom.objects.get(id = int(request.POST['EduDiplomType'])) if request.POST['EduDiplomType'] else None
    a.EduEducationType = EduType.objects.get(id = int(request.POST['EduEducationType'])) if request.POST['EduEducationType'] else None


    a.EduDateIN  = valid_date(request.POST['EduDateIN'])  if request.POST['EduDateIN']  else None
    a.EduDateOUT = valid_date(request.POST['EduDateOUT']) if request.POST['EduDateOUT'] else None

    a.EduDiplomspeciality = request.POST['EduDiplomspeciality']
    a.EduSeriaDiplom      = request.POST['EduSeriaDiplom']
    a.EduNumberDiplom     = request.POST['EduNumberDiplom']

    Exam.objects.filter(user = a.user).delete()

    for i in range(min( len(request.POST.getlist('EgNumber[]')), 5 ) ):
        e = Exam()
        e.user     = a.user
        e.Number   = request.POST.getlist('EgNumber[]')[i]
        e.ExamName = ExamName.objects.get(id = int(request.POST.getlist('EgExamName[]')[i])) if request.POST.getlist('EgExamName[]')[i] else None
        e.Mark     = int(request.POST.getlist('EgMark[]')[i])     if request.POST.getlist('EgMark[]')[i]     else None
        e.DocSer   = int(request.POST.getlist('EgDocSer[]')[i]) if request.POST.getlist('EgDocSer[]')[i] else None
        e.DocNum   = int(request.POST.getlist('EgDocNum[]')[i])    if request.POST.getlist('EgDocNum[]')[i] else None
        e.save()

    a.UlsuIDStructure = ULSUCource.objects.get(id = int(request.POST['UlsuIDStructure'])) if request.POST['UlsuIDStructure'] else None
    a.UlsuDateIn      = request.POST['UlsuDateIn']  if request.POST['UlsuDateIn']  else None
    a.UlsuDateOut     = request.POST['UlsuDateOut'] if request.POST['UlsuDateOut'] else None

    save_fachs(request, a)

    if request.user.groups.filter(name='Publisher'):
        a.Original = ('Original' in request.POST)

    a.save()






@login_required
def save_form(request):
    if request.method != 'POST':
        raise Http404

    a = None

    is_publisher  = request.user.groups.filter(name='Publisher')
    is_automech   = request.user.groups.filter(name='Automech')
    is_comp_class = request.user.groups.filter(name='computer_class')

    approve = False
    if 'approve' in request.POST and request.POST['approve'] == '1':
        approve = True

    edit_ = False
    if 'user_id' in request.POST:
        try:
            edit_id = int(request.POST['user_id'])
            a = Application.objects.get(user_id = edit_id)
        except:
            edit_ = False
        else:
            edit_ = True


    if is_comp_class or (is_publisher and not edit_):
        user = temp_user()

        try:
            a = Application.objects.get(user = user)
        except:
            a = Application()
            a.user = user
            a.save()

        user = User()
        user.username = 'user_' + str(a.id)
        user.set_unusable_password()
        user.save()
        a.user = user
        a.save()
    elif not is_publisher:
        try:
            a = Application.objects.get(user = request.user)
        except:
            a = Application()
            a.user = request.user
            a.save()

    if a is None:
        raise Http404

    if a.Approved:
        if not is_publisher:
            raise Http404
        else:
            save_approved(request, a)
            return send_to_gusarov(a)
    else:
        do_save(request, a)
        if approve:
            return send_to_gusarov(a)
            a.Approved = True
            a.approve_date = datetime.now()
            a.save()

        if is_publisher:
            log = Add()
            log.user = request.user
            log.app = a
            if is_automech:
                log.automech = True
            log.save()
    return redirect('/accounts/personal/')




def save_fachs(request, a):
    if not a.Approved:
        Fach.objects.filter(user = a.user).delete()

    specRanges = real_ranges(request.POST.getlist('SpecRange[]')[:])

    for i in range(min(len(request.POST.getlist('SpecItem[]')), 3)):
        fach = Fach()
        fach.user = a.user

        if request.POST.getlist('Speciality[]')[i]:
            try:
                s = Speciality.objects.get(id = int(request.POST.getlist('Speciality[]')[i]))
            except:
                pass
            else:
                fach.speciality = s
                fach.save()

            try:
                f = Faculty.objects.get(id = int(request.POST.getlist('Faculty[]')[i]))
                specfac = SpecialityFaculty.objects.filter(speciality = s, faculty = f)
            except:
                break
            else:
                fach.faculty = f
                fach.save()

            efs = request.POST.getlist('EduForm[]')[i].split(',')
            for ef in efs:
                try:
                    e = EduForm.objects.get(id = int(ef))
                    MainSpec.objects.get(speciality_faculty = specfac, edu_form = e)
                except:
                    break
                else:
                    fach.edu_form.add(e)

        fach.Priority   = specRanges[i] if specRanges[i] else None
        fach.Stream     = int(request.POST.getlist('SpecStream[]')[i])               if request.POST.getlist('SpecStream[]')[i]    else None
        fach.Service    = int(request.POST.getlist('SpecLengthServiceSpecial[]')[i]) if request.POST.getlist('SpecLengthServiceSpecial[]')[i]  else None
        fach.save()



def safe_str(v, t=None):
    try:
        if t is None:
            val = v
        elif t == 'id':
            val = v.id
        elif t == 'name':
            val = v.name
        elif t == 'type':
            val = v.type
        else:
            return 'NULL'
    except:
        return 'NULL'
    else:
        if val:
            return "'%s'" % val
        else:
            return 'NULL'

def unsafe_str(v, t=None):
    try:
        if t is None:
            val = v
        elif t == 'id':
            val = v.id
        elif t == 'name':
            val = v.name
        elif t == 'type':
            val = v.type
        else:
            raise Http404
    except:
        raise Http404
    else:
        if val:
            return "'%s'" % val
        else:
            raise Http404

def save_approved(request, a):
    save_fachs(request, a)
    if request.user.groups.filter(name='Publisher'):
        a.Original = ('Original' in request.POST)
    a.save()


def unsafe_int(v):
    try:
        val = int(v)
    except:
        raise Http404
    else:
        return str(val)


def unsafe_id(v):
    try:
        u = unsafe_int(v.id)
    except:
        raise Http404
    else:
        return str(u)


def unsafe_name(v):
    try:
        i = v.name
    except:
        raise Http404
    else:
        return "'%s'" % i


def unsafe(v):
    if v:
        return "'%s'" % v
    else:
        raise Http404


def send_to_gusarov(a):
    e = Exam.objects.filter(user = a.user)
    f = Fach.objects.filter(user = a.user)

    qdict = {
        # Обязательные поля
        'Citizenship':    unsafe_name(a.Citizenship),
        'IDSex':          str(int(a.IDSex)),
        'Nationality':    unsafe_name(a.Nationality),
        'IDSocialStatus': unsafe_id(a.IDSocialStatus),

        'IDMilitaryService': unsafe_id(a.IDMilitaryService),

        'BirthDay': unsafe(a.BirthDay),
        'Hostel': str(int(a.Hostel)),
        'PassportDate': unsafe(a.PassportDate),
        'IDInstitute': '1',
        'DateINSchool': unsafe(a.EduDateIN),
        'DateOUTSchool': unsafe(a.EduDateOUT),
        'IDEducationSpeciality': '1',
        'IDStructureF': '1',
        #'SendDate': unsafe(a.approve_date),


        'CountryPass': safe_str(a.PrCountry, 'name'),
        'RegionPass':  safe_str(a.PrRegion, 'name'),
        'RegionAreaPass': "'%s'" % a.PrRegionArea.name if a.PrRegionArea else u"'Нет района'",
        'LocalityTypePass': safe_str(a.PrLocality, 'type'),
        'LocalityPass':     safe_str(a.PrLocality, 'name'),
        'CityAreaPass': 'NULL',
        'StreetType': '1', #!!!!!!!!!!!!!!!!!!!!!!!!!!!
        'StreetPass': safe_str(a.PrStreet, 'name'),
        'IndexPass':  safe_str(a.PrIndex),
        'HousePass':  safe_str(a.PrHouse),
        'AppartmentPass': safe_str(a.PrApartment),


        'ForeignLanguage': unsafe_id(a.ForeignLanguage),
        'FirstName':  safe_str(a.FirstName),
        'LastName':   safe_str(a.LastName),
        'MiddleName': safe_str(a.MiddleName),
        'BirthPlace': safe_str(a.BirthPlace),
        'Telephone':  safe_str(a.Telephone),
        'Email':      safe_str(a.Email),
        'LengthServiceTotal': safe_str(a.LengthServiceTotal),

        'PassportSer':    safe_str(a.PassportSer),
        'PassportNumb':   safe_str(a.PassportNumb),
        'PassportIssued': safe_str(a.PassportIssued),
        'CodeUVD':        safe_str(''.join(a.CodUVD.split('-'))) if a.CodUVD else 'NULL',
        'IDPrivileges':   safe_str(a.PrivIDPrivileges, 'id'),

        'DiplomType':       safe_str(a.EduDiplomType, 'name'),
        'EducationType':    safe_str(a.EduEducationType, 'name'),
        'Diplomspeciality': safe_str(a.EduDiplomspeciality),
        'SeriaDiplom':      safe_str(a.EduSeriaDiplom),
        'NumberDiplom':     safe_str(a.EduNumberDiplom),
        'IDStructure':      safe_str(a.UlsuIDStructure, 'id'),
        'DateIn':   safe_str(a.UlsuDateIn),
        'DateOut':  safe_str(a.UlsuDateOut),
        'SendDate': safe_str(datetime.now().strftime('%Y-%m-%d'))
    }


    if not a.schoolSel:
        qdict['IDInstitute'] = '"%s"' % a.schoolName.id if a.schoolName else '0'
        qdict['CountrySchool'] =        'NULL'
        qdict['RegionAreaSchool'] =     'NULL'
        qdict['RegionSchool'] =         'NULL'
        qdict['LocalityTypeSchool'] =   'NULL'
        qdict['LocalitySchool'] =       'NULL'
        qdict['InstituteType'] =        'NULL'
        qdict['InstituteName'] =        'NULL'
        qdict['InstituteDescription'] = 'NULL'
    else:
        qdict['IDInstitute'] = '0'
        qdict['CountrySchool'] =        safe_str(a.EduCountry, 'name')
        qdict['RegionAreaSchool'] = "'%s'" % a.EduRegionArea.name if a.EduRegionArea else u"'Нет района'"
        qdict['RegionSchool'] =         safe_str(a.EduRegion, 'name')
        qdict['LocalityTypeSchool'] =   safe_str(a.EduLocality, 'type')
        qdict['LocalitySchool'] =       safe_str(a.EduLocality, 'name')
        qdict['InstituteType'] =        safe_str(a.EduInstituteType, 'name')
        qdict['InstituteName'] =        safe_str(a.EduInstituteName)
        qdict['InstituteDescription'] = safe_str(a.EduInstituteDescription)

    qdict['CityAreaSchool'] =   'NULL'
    qdict['StreetSchool'] =     'NULL'
    qdict['IndexSchool'] =      'NULL'
    qdict['HouseSchool'] =      'NULL'
    qdict['AppartmentSchool'] = 'NULL'

    if a.prp:
        qdict['LiveCityArea'] =   'NULL'
        qdict['LiveStreet'] =     safe_str(a.LiveStreet, 'name')
        qdict['LiveHouse'] =      safe_str(a.LiveHouse)
        qdict['LiveAppartment'] = safe_str(a.LiveApartment)
    else:
        qdict['LiveCityArea'] =  'NULL'
        qdict['LiveStreet'] =    'NULL'
        qdict['LiveHouse'] =     'NULL'
        qdict['LiveAppartment'] ='NULL'

    for i in range(1,6):
        if i in e:
            qdict['Number'+str(i)] =   e[i].Number
            qdict['ExamName'+str(i)] = e[i].ExamName.name
            qdict['Mark'+str(i)] =     e[i].Mark
            qdict['DocSer'+str(i)] =   e[i].DocSer
            qdict['DocNum'+str(i)] =   e[i].DocNum
        else:
            qdict['Number'+str(i)] =   'NULL'
            qdict['ExamName'+str(i)] = 'NULL'
            qdict['Mark'+str(i)] =     'NULL'
            qdict['DocSer'+str(i)] =   'NULL'
            qdict['DocNum'+str(i)] =   'NULL'



    for i in range(1,6):
        qdict['USExamName'+str(i)] = 'NULL'


    f = Fach.objects.filter(user = a.user)

    c = pyodbc.connect("DSN=OpenLink;UID=webit;PWD=it123;")
    cursor = c.cursor()

    for i in range(len(f)):
        for j in f[i].edu_form.all():
            # sf = SpecialityFaculty.objects.get(speciality=f[i].speciality, faculty=f[i].faculty)
            # spec = MainSpec.objects.get(speciality_faculty=sf, edu_form=j)
            # qdict['IDEducationSpeciality'] = str(spec.mainspec_id)
            # qdict['IDStructureEducForm'] = str(j.id)
            # qdict['IDSpecial'] = str(spec.mainspec_id)
            # qdict['IDStructureF'] = 'NULL' #!!!!!!!!!!!!!!!!!!!!!
            # qdict['IDRightSemiPassMark'] = 'NULL' #!!!!!!!!!!!!!!!!!
            # qdict['LengthServiceSpecial'] = safe_str(f[i].Service)
            qdict['Stream'] = safe_str(f[i].Stream)
            # qdict['Range'] = safe_str(f[i].Priority)


            query = generate_query(qdict)
            #return print_r(query)
            cursor.execute(query.encode('cp1251'))
            c.commit()
            c.close()

            return HttpResponse(query)

    #c.close()
    return HttpResponse('Ready')


def generate_query(qdict):
    arrkey = []
    arrval = []

    for i in qdict:
        arrkey.append('['+i+']')
        arrval.append(qdict[i])

    query = 'INSERT INTO [dbo].[AbitInternet] (' + ','.join(arrkey) + ') VALUES (' + ','.join(arrval) + ')'
    return query

def test_mssql(request):
    c = pyodbc.connect("Driver=/usr/local/lib/libtdsodbc.so;Server=10.1.0.80;UID=webit;PWD=it123;PORT=1433;DATABASE=Base13Test;TDS_VERSION=8.0;charset=cp1251;")


@login_required
def show_list(request):
    t = loader.get_template("list.html")
    c = RequestContext(request, {'users': Application.objects.all()})
    return HttpResponse(t.render(c))


@login_required
def edit(request, user):
    if request.user.groups.filter(name='Publisher'):
        app = Application.objects.filter(id = user)
        if app:
            return show_form(request, app[0])
        else:
            raise Http404
    else:
        raise Http404

def print_r(var):
    return HttpResponse( Template( "<pre>{{var}}</pre>" ).render( Context( {'var':var} ) ) )