# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context, RequestContext, Template
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from models import *
from form.models import Application, ExamSpec, MainSpec
import random
import string
from django.conf import settings
from django.utils import timezone
import datetime
from django.http import Http404
from django.contrib import auth
from django.shortcuts import redirect
from django.views.static import serve
import xlwt, xlrd
from django.views.static import serve


def dev(function_to_decorate):
    def func(request, *args, **kwargs):
        if False and settings.DEBUG and request.user.is_anonymous and request.META['HTTP_X_FORWARDED_FOR'] != '62.76.32.162':
            raise Http404
        else:
            return function_to_decorate(request, *args, **kwargs)
    return func


def xls(request, ab):
    """
    Получает студента и выводит xls-файл с его данными для печати.
    Для работы требуется библиотека xlwt

    В этой функции очень много xlwt-магии, которая завязана на особой Майкрософтовой Excel-магии.
    Размер шрифта нада умножать на 20.
    Ширину столбцов надо подгонять руками и измеряются они чёрт знает в чём.
    Высота строк не задаётся через row.height, нужно ко всей строке применять стиль с размером шрифта, который надо
    подгонять под требуемый размер.

    Стили ячеек сделаны через easyxf (а должны по сути быть сделаны на объектах Style),потому что я не нашёл, как
    в объектах задавать цвет шрифта. Я не знаю, зачем для ч/б распечатывания ИМ понадобился цветной заголовок.


    """
    #return HttpResponse(ab)
    a = Application.objects.get(id=ab)

    style = {
        #УЛЬЯНОВСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ
        'h1': xlwt.easyxf('font: height 280, name Times, colour_index dark_blue, bold True; align: vert bottom, horiz centre;'),
        #СВЕДЕНИЯ ОБ АБИТУРИЕНТЕ
        'h2': xlwt.easyxf('font: height 240, name Times, colour_index dark_blue, bold True; align: vert bottom, horiz centre;'),

        #Ф.И.О.:
        'namek': xlwt.easyxf('font: height 240, name Times, bold True, italic True; align: vert bottom, horiz left; border: top thin;'),
        #Имя абитуриента
        'namev': xlwt.easyxf('font: height 280, name Times, bold True; align: vert bottom, horiz left; border: top thin;'),

        #Пустая строка с нижним пожчёркиванием
        'bt': xlwt.easyxf('border: bottom thin;'),

        #Графа
        'dd': xlwt.easyxf('font: height 240, name Times, bold True, italic True; border: bottom hair; align:vert top;'),
        #Значение
        'dt': xlwt.easyxf('font: height 240, name Times; border: bottom hair; align: wrap True, vert top;'),

        #Графа со сплошной линией внизу
        'dd-bt': xlwt.easyxf('font: height 240, name Times, bold True, italic True; border: bottom thin; align: vert top, horiz left;'),
        #Значение со сплошной линией внизу
        'dt-bt': xlwt.easyxf('font: height 240, name Times; border: bottom thin; align: vert top, horiz left;'),

        #ИНФОРМАЦИЯ О ПОДАННЫХ ЗАЯВЛЕНИЯХ
        'h3': xlwt.easyxf('font: height 240, name Times, bold True, italic True; align: vert bottom, horiz centre; border: bottom thin;'),
        #Заголовок таблицы с информацией о поданных заявлениях (THead-Fach)
        'th-f': xlwt.easyxf('font: height 240, name Times, bold True, italic True; align: vert centre, horiz centre; border: bottom thin, right hair, left hair;'),
        #Заголовок таблицы с информацией о поданных заявлениях с большим текстом, который не умещается и в связи с этим имеет размер шрифта 10 (THead-Fach-Small)
        'th-f-s': xlwt.easyxf('font: height 200, name Times, bold True, italic True; align: wrap True, vert centre, horiz left; border: bottom thin, right hair, left hair;'),
        #Строка таблицы с информацией о поданных заявлениях (TBody-Fach)
        'tb-f': xlwt.easyxf('font: height 200, name Times, bold True, italic True; align: wrap True, vert top, horiz left; border: bottom hair, right hair, left hair;'),

        #Заголовок таблицы с ЕГЭ
        'th-e': xlwt.easyxf('font: height 240, name Times, bold True, italic True; border: bottom hair;'),
        #Заголовок таблицы с ЕГЭ и выравниванием по центру
        'th-e-с': xlwt.easyxf('font: height 240, name Times, bold True, italic True; border: bottom hair; align: vert top, horiz centre;'),

        #Тело таблицы с ЕГЭ
        'tb-e': xlwt.easyxf('font: height 200, name Times;  align: vert top, horiz left;'),
        #Тело таблицы с ЕГЭ и выравниванием по центру
        'tb-e-с': xlwt.easyxf('font: height 200, name Times; align: vert top, horiz centre;'),

        #Заголовок таблицы с заявками на сдачу ЕГЭ
        'th-z': xlwt.easyxf('font: height 240, name Times, bold True, italic True; align: vert top, horiz centre; border: bottom hair, top thin;'),
        #Тело таблицы с заявками на сдачу ЕГЭ
        'tb-z': xlwt.easyxf('font: height 200, name Times; border: bottom hair;'),

        #Графа без подчёркивания (Without Border)
        'dd-wb': xlwt.easyxf('font: height 240, name Times, bold True, italic True; align:vert top;'),
        #Графа без подчёркивания (Without Border, Align Right)
        'dd-wb-ar': xlwt.easyxf('font: height 240, name Times, bold True, italic True; align:vert top, horiz right;'),
        #Значение без подчёркивания (Without Border)
        'dt-wb': xlwt.easyxf('font: height 240, name Times; align: wrap True, vert top;'),
    }

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet('A Test Sheet')

    cols = [331, 312, 276, 272, 300, 300]
    for i in range(len(cols)):
        col = ws.col(i)
        col.width = cols[i] * 20

    rows = {
        3: 935,
        4: 840,
        11: 630,
        19: 930,
        26: 290,
        27: 290,
        28: 290,
        29: 290,
        30: 290,
        31: 290,
        33: 290,
        34: 290,
        35: 290,
        36: 290,
        37: 290,
        38: 290,
        46: 517
    }
    for i in rows:
        row = ws.row(i)
        row.set_style(xlwt.easyxf('font:height %s;' % rows[i]))

    ws.write_merge(0, 0, 0, 3, 'УЛЬЯНОВСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ', style['h1'])
    ws.write_merge(1, 1, 0, 3, 'СВЕДЕНИЯ ОБ АБИТУРИЕНТЕ', style['h2'])

    r = ws.row(3)

    ws.write(3, 0, 'Ф.И.О.:', style['namek'])
    ws.write(3, 1, a.LastName + ' ' + a.FirstName + ' ' + a.MiddleName, style['namev'])
    ws.write(3, 2, '', style['namev'])

    ws.write(4, 0, '', style['bt'])
    ws.write(4, 1, '', style['bt'])
    ws.write(4, 2, '', style['bt'])


    ws.write(5, 0, 'Дата рождения:', style['dd'])
    ws.write(5, 1, a.BirthDay.strftime('%d.%m.%Y'), style['dt'])
    ws.write(5, 2, '', style['bt'])
    ws.write(5, 3, '', style['dt'])

    ws.write(6, 0, 'Пол:', style['dd'])
    ws.write(6, 1, a.get_IDSex_display(), style['dt'])
    ws.write(6, 2, 'Паспорт:', style['dd'])
    ws.write(6, 3, str(a.PassportSer) + ' ' + str(a.PassportNumb), style['dt'])

    ws.write(7, 0, 'Национальность:', style['dd'])
    ws.write(7, 1, a.Nationality.name, style['dt'])
    ws.write(7, 2, 'Гражданство:', style['dd'])
    ws.write(7, 3, a.Citizenship.name, style['dt'])

    ws.write(8, 0, 'Адрес прописки:', style['dd'])
    ws.write(8, 1, a.PrRegion.name, style['dt'])
    ws.write(8, 2, '---', style['dt'])
    ws.write(8, 3, a.PrLocality.type + '. ' + a.PrLocality.name, style['dt'])
    ws.write(9, 1, a.PrStreet.type + '. ' + a.PrStreet.name, style['dt'])
    ws.write(9, 2, u'д.' + a.PrHouse, style['dt'])
    ws.write(9, 3, u'кв.' + a.PrApartment, style['dt'])

    ws.write(10, 0, 'Местный адрес:', style['dd'])
    ws.write(10, 1, a.PrStreet.type + '. ' + a.PrStreet.name + ' ' + a.PrHouse + ' - ' + a.PrApartment, style['dt'])
    ws.write(10, 2, '', style['dt'])
    ws.write(10, 3, '', style['dt'])

    #border: Bottom Thin;
    ws.write(11, 0, 'Индекс:', style['dd-bt'])
    ws.write(11, 1, a.PrIndex, style['dt-bt'])
    ws.write(11, 2, 'Телефон:', style['dd-bt'])
    ws.write(11, 3, a.Telephone, style['dt-bt'])

    ws.write(12, 0, 'Общежитие:', style['dd'])
    ws.write(12, 1, 'требуется' if a.Hostel else 'не требуется', style['dt'])
    ws.write(12, 2, '', style['dt'])
    ws.write(12, 3, '', style['dt'])

    ws.write(13, 0, 'Воинск. обязанность:', style['dd'])
    ws.write(13, 1, a.IDMilitaryService.name if a.IDMilitaryService else '', style['dt'])
    ws.write(13, 2, '', style['dt'])
    ws.write(13, 3, '', style['dt'])

    ws.write(14, 0, 'Льготы:', style['dd'])
    ws.write_merge(14, 14, 1, 3, a.PrivIDPrivileges.name if a.PrivIDPrivileges else '', style['dt'])

    #TODO: запилить в форму селект "право при полупроходном балле"
    #border: Bottom Thin;
    ws.write(15, 0, 'Право при п/п балле:', style['dd-bt'])
    ws.write_merge(15, 15, 1, 3, '', style['dt-bt'])

    ws.write(16, 0, 'Образование:', style['dd'])
    if not a.schoolSel:
        ws.write(16, 1, a.schoolCity.name, style['dt'])
        ws.write(16, 2, a.schoolName.name, style['dt'])
    else:
        ws.write(16, 1, a.EduLocality.name, style['dt'])
        ws.write(16, 2, a.EduInstituteName, style['dt'])
    ws.write(16, 3, a.EduDateIN.strftime('%Y') + '-' + a.EduDateOUT.strftime('%Y'), style['dt'])

    ws.write(17, 0, 'Тип,сер.,ном.дипл./ат.:', style['dd-bt'])
    ws.write(17, 1, a.EduDiplomType.name, style['dt-bt'])
    ws.write(17, 2, a.EduSeriaDiplom, style['dt-bt'])
    ws.write(17, 3, a.EduNumberDiplom, style['dt-bt'])

    ws.write_merge(18, 18, 0, 3, 'ИНФОРМАЦИЯ О ПОДАННЫХ ЗАЯВЛЕНИЯХ', style['h3'])

    ws.write(19, 0, 'Факультет', style['th-f'])
    ws.write(19, 1, 'Специальность', style['th-f'])
    ws.write(19, 2, 'Форма обучения', style['th-f'])
    ws.write(19, 3, 'Приоритет (только для бюджетной формы обучения)', style['th-f-s'])

    i = 20      # Индекс первой строки со специальностями
    j = 0       # Счётчик выведенных в таблицу специальностей
    Fachs = Fach.objects.filter(user=a.user).order_by('Priority')  # Список заявок, поданных абитуриентом
    if not Fachs:
        i += 5
    else:
        m = 1 #Приоритет
        for f in Fachs: #Выводим специальность
            for form in f.edu_form.all():
                ws.write(i, 0, f.fac_name.name, style['tb-f'])
                ws.write(i, 1, f.spec_name.name, style['tb-f'])
                ws.write(i, 2, form.name, style['tb-f'])
                ws.write(i, 3, str(m), style['tb-f'])
                j += 1
                i += 1
            m += 1

        while j<5:
            ws.write(i, 0, '', style['tb-f'])
            ws.write(i, 1, '', style['tb-f'])
            ws.write(i, 2, '', style['tb-f'])
            ws.write(i, 3, '', style['tb-f'])
            i += 1
            j += 1

    ws.write_merge(i, i, 0, 1, 'Заявка на сдачу ЕГЭ:', style['th-z'])
    ws.write_merge(i, i, 2, 3, 'Дата экзамена ЕГЭ:', style['th-z'])

    j = 0
    i += 1
    while j<6:
        ws.write_merge(i, i, 0, 1, '', style['tb-z'])
        ws.write_merge(i, i, 2, 3, '', style['tb-z'])
        j += 1
        i += 1

    ws.write(i, 0, 'Подг. отделен. УлГУ:', style['dd'])
    ws.write(i, 1, a.UlsuIDStructure.name if a.UlsuIDStructure else '', style['dt'])
    ws.write(i, 2, '', style['dt'])
    ws.write(i, 3, '', style['dt'])

    ws.write(i+1, 0, 'Иностран. язык:', style['dd-bt'])
    ws.write(i+1, 1, a.ForeignLanguage.name if a.ForeignLanguage else '', style['dt-bt'])
    ws.write(i+1, 2, '', style['dt-bt'])
    ws.write(i+1, 3, '', style['dt-bt'])

    ws.write_merge(i+2, i+2, 0, 1, 'Общий стаж работы в полных месяцах:', style['dd'])
    ws.write(i+2, 2, str(a.LengthServiceTotal), style['dt'])
    ws.write(i+2, 3, '', style['dt'])

    ws.write_merge(i+3, i+3, 0, 1, 'Общий стаж работы по специальности:', style['dd-bt'])
    ws.write(i+3, 2, '0', style['dt-bt'])
    ws.write(i+3, 3, '', style['dt-bt'])

    ws.write_merge(i+6, i+6, 0, 1, 'Подпись и фамилия сотрудника ПК:', style['dd-wb'])

    ws.write(i+8, 0, 'Подпись абитуриента:', style['dd-wb'])
    ws.write(i+8, 2, 'Дата:', style['dd-wb-ar'])
    ws.write(i+8, 3, datetime.datetime.now().strftime('%d.%m.%Y'), style['dt-wb'])

    ws.insert_bitmap('/django/django-apps/abiturient/staticfiles/image/photo.bmp', 2, 3)

    fname = 'testfile.xls'
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    wb.save(response)
    return response

RUS  = ExamSpec.objects.get(id=1)
ALG  = ExamSpec.objects.get(id=2)
MATH = ExamSpec.objects.get(id=6)


@dev
def hello(request):
    var = True if 'var' in request.COOKIES and int(request.COOKIES['var']) == 1 else False

    ex = ExamSpec.objects.filter(in_list=True)
    exams = []
    for e in ex:
        if not e in [RUS, MATH, ALG]:
            exams.append(e)


    t = loader.get_template("test.html")
    c = RequestContext(request, {'var': var, 'exams': exams})
    return HttpResponse(t.render(c))


@dev
def logout(request):
    auth.logout(request)
    return redirect('/')
     
    
@csrf_exempt
@dev
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            auth.login(request, user)
        else:
            return redirect('/accounts/login/?error=1')
        if request.POST['next']:
            return redirect(request.POST['next'])
        else:
            return redirect('/')
            
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
        
    next = request.GET['next'] if 'next' in request.GET else '/'
    t = loader.get_template("login.html")
    c = RequestContext(request, {'var': var, 'next': next})
    return HttpResponse(t.render(c))
    
    
@csrf_exempt
@dev
def register(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False

    t = loader.get_template("register.html")
    if request.method == 'POST':
        if 'email' in request.POST and request.POST['email']!='':
            a = User()
            a.username = request.POST['email']
            a.email = request.POST['email']
            password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(10))
            a.set_password(password)
            a.is_active = True
            a.save()

            ctx_dict = {
                'password': password,
                'login': request.POST['email'],
                'site': 'http://abiturient.ulsu.ru/',
            }
                    
            subject = loader.render_to_string('registration/activation_email_subject.txt', ctx_dict)

            subject = ''.join(subject.splitlines())
        
            message = loader.render_to_string('registration/activation_email.txt', ctx_dict)
        
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, (a.email,))

            t = loader.get_template("register_done.html")

    c = RequestContext(request, {'var': var})
    return HttpResponse(t.render(c))


def parse_exams(array):
    new_array = []
    for i in array:
        try:
            a = ExamSpec.objects.get(id=int(i))
        except:
            pass
        else:
            new_array.append(a)
    return new_array


def compare_exams(first, second):
    for s in second:
        if not s in first:
            return False
    return True




@csrf_exempt
@dev
def my_speciality(request):

    if request.method != 'POST':
        raise Http404

    try:
        edu_raw = int(request.POST['edu'])
        edu_high = (edu_raw == 1)
    except:
        raise Http404

    if edu_high:
        my_exams_arr = [RUS, MATH]
    else:
        my_exams_arr = [RUS, ALG]

    my_exams = parse_exams(request.POST.getlist('exam[]')) + my_exams_arr

    acc_mainspecs = []
    mainspecs = MainSpec.objects.all()
    for m in mainspecs:
        if compare_exams(my_exams, m.exams.all()):
            acc_mainspecs.append(m)


    specs = {}
    for am in acc_mainspecs:
        sf = am.speciality_faculty
        if not sf.speciality.id in specs:
            specs[sf.speciality.id] = {'speciality': sf.speciality, 'faculties': {}}
        if not sf.faculty.id in specs[sf.speciality.id]['faculties']:
            specs[sf.speciality.id]['faculties'][sf.faculty.id] = {'faculty': sf.faculty, 'edu_forms': []}
        if am.edu_form.school and (edu_high or am.edu_form.spo):
            specs[sf.speciality.id]['faculties'][sf.faculty.id]['edu_forms'].append(am.edu_form)

    specialities = []
    for s in specs:
        facs = []
        for f in specs[s]['faculties']:
            if specs[s]['faculties'][f]['edu_forms']:
                facs.append(specs[s]['faculties'][f])
        if facs:
            specialities.append({'speciality': specs[s]['speciality'], 'faculties': facs})


    t = loader.get_template("my_speciality.html")
    c = RequestContext(request, {'specialities': specialities, 'exams': my_exams})
    return HttpResponse(t.render(c))

    
def mediaserver(request, path):
    return serve(request, path, settings.MEDIA_ROOT)
