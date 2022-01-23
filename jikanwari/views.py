from django.shortcuts import render, redirect
from django.views import View
from .models import Class, Settings, Assignments
from .forms import ClassForm, SettingsForm, AssignmentForm, AssignmentsForm
from datetime import datetime, timedelta, date, time
import time as tm
import webbrowser
import schedule
import threading


def main(request):
    if not Settings.objects.filter().exists():
        Settings.objects.create()
    setting = Settings.objects.get()
    #if the user decided to use this function, activate open_link in a new thread
    if setting.open_link:
        stop = True
        stop = False
        th1 = threading.Thread(target=open_link)
        th1.start()
    dic = {}
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    periods = ['1', '2', '3', '4', '5', '6', '7']
    for period in periods:
        for day in days:
            s = day + period
            if not Class.objects.filter(day_period=s).exists():
                Class.objects.create(
                    name = '',
                    url = '', 
                    memo = '',
                    day_period = s,
                    color = '#FFFFFF'
                )
            dic[s] = query_into_dic(Class.objects.get(day_period=s))
    if not Settings.objects.filter().exists():
        Settings.objects.create(
            sat = False,
            sun = False,
            open_link = False,
            period = 5
        )
    sett = Settings.objects.get()
    dic['settings'] = {
        'sat': sett.sat,
        'sun': sett.sun,
        'period': sett.period,
        's1': sett.s1,
        'e1': sett.e1,
        's2': sett.s2,
        'e2': sett.e2,
        's3': sett.s3,
        'e3': sett.e3,
        's4': sett.s4,
        'e4': sett.e4,
        's5': sett.s5,
        'e5': sett.e5,
        's6': sett.s6,
        'e6': sett.e6,
        's7': sett.s7,
        'e7': sett.e7
    }
    times = []
    periods = []
    if sett.s1 is not None:
        times.append(sett.s1.strftime('%H:%M'))
        periods.append('1')
    if sett.s2 is not None:
        times.append(sett.s2.strftime('%H:%M'))
        periods.append('2')
    if sett.s3 is not None:
        times.append(sett.s3.strftime('%H:%M'))
        periods.append('3')
    if sett.s4 is not None:
        times.append(sett.s4.strftime('%H:%M'))
        periods.append('4')
    if sett.s5 is not None:
        times.append(sett.s5.strftime('%H:%M'))
        periods.append('5')
    if sett.s6 is not None:
        times.append(sett.s6.strftime('%H:%M'))
        periods.append('6')
    if sett.s7 is not None:
        times.append(sett.s7.strftime('%H:%M'))
        periods.append('7')
    dic['classdata'] = []
    for period, time in zip(periods, times):
        for day in days:
            s = day + period
            c = Class.objects.get(day_period=s)
            if c.url != '':
                dic['classdata'].append({'time':day + " " + time, 'url':c.url})
    if sett.sat:
        if sett.sun:
            width = {'h': 5.5, 'd': 13.5}
        else:
            width = {'h': 4, 'd': 16}
    else:
        if sett.sun:
            width = {'h': 4, 'd': 16}
        else:
            width = {'h': 5, 'd': 19}
    dic['width'] = width
    return render(request, 'jikanwari/main.html', dic)


def query_into_dic(q):
    d = {
        'name': q.name,
        'url': q.url,
        'memo': q.memo,
        'color': q.color,
    }
    return d


def edit(request, s):
    obj = Class.objects.get(day_period=s)
    initial_dict = {
        'name': obj.name,
        'url': obj.url,
        'memo': obj.memo,
        'color': obj.color,
    }
    form = ClassForm(request.POST or None, initial=initial_dict)

    if request.method == 'POST':
        if 'save' in request.POST:
            if form.is_valid():
                Class.objects.filter(day_period=s).delete()

                Class.objects.create(
                    name = form.cleaned_data['name'], 
                    url = form.cleaned_data['url'], 
                    memo = form.cleaned_data['memo'], 
                    color = form.cleaned_data['color'],
                    day_period = s
                )
                return redirect('main')
        elif 'delete' in request.POST:
            Class.objects.filter(day_period=s).delete()
            return redirect('main')
    return render(request, 'jikanwari/edit.html', {'form': form})


def settings(request):
    obj = Settings.objects.get()
    initial_dict = {
        'sat': obj.sat,
        'sun': obj.sun,
        'period': obj.period,
        'open_link': obj.open_link
    }
    names = ['s1', 'e1', 's2', 'e2', 's3', 'e3', 's4', 'e4', 's5', 'e5', 's6', 'e6', 's7', 'e7']
    times = [obj.s1, obj.e1, obj.s2, obj.e2, obj.s3, obj.e3, obj.s4, obj.e4, obj.s5, obj.e5, obj.s6, obj.e6, obj.s7, obj.e7]
    for name, time in zip(names, times):
        if time != None:
            initial_dict[name] = time.strftime('%H:%M')
        else:
            initial_dict[name] = time
    form = SettingsForm(request.POST or None, initial=initial_dict)

    if form.is_valid():
        Settings.objects.filter().delete()

        Settings.objects.create(
            sat = form.cleaned_data['sat'], 
            sun = form.cleaned_data['sun'], 
            period = form.cleaned_data['period'],
            s1 = form.cleaned_data['s1'],
            e1 = form.cleaned_data['e1'],
            s2 = form.cleaned_data['s2'],
            e2 = form.cleaned_data['e2'],
            s3 = form.cleaned_data['s3'],
            e3 = form.cleaned_data['e3'],
            s4 = form.cleaned_data['s4'],
            e4 = form.cleaned_data['e4'],
            s5 = form.cleaned_data['s5'],
            e5 = form.cleaned_data['e5'],
            s6 = form.cleaned_data['s6'],
            e6 = form.cleaned_data['e6'],
            s7 = form.cleaned_data['s7'],
            e7 = form.cleaned_data['e7'],
            open_link = form.cleaned_data['open_link']
        )
        return redirect('main')
    return render(request, 'jikanwari/settings.html', {'form': form})


def assignments(request):
    obj = Assignments.objects.order_by('deadline')
    # if request.method == 'POST':
    #     for o in obj:
    #         if o.pk in request.POST:
    #             Assignments.objects.filter(pk=o.pk).delete()
    num_to_day = {
        0: '月',
        1: '火',
        2: '水',
        3: '木',
        4: '金',
        5: '土',
        6: '日'
    }
    check = False
    if not obj.exists():
        check = True
    else:
        for o in obj:
            o.deadline += timedelta(hours=9)
            o.deadline = o.deadline.strftime("%m/%d") + '（' + num_to_day[o.deadline.weekday()] + '）' + o.deadline.strftime("%H:%M")
    dic = {'obj': obj, 'check': check}
    return render(request, 'jikanwari/assignments.html', dic)


def edit_assignment(request, pk):
    obj = Assignments.objects.get(pk=pk)
    initial_dict = {
        'deadline': obj.deadline,
        'subject': obj.subject,
        'memo': obj.memo,
        'color': obj.color,
        'label': obj.label,
    }
    form = AssignmentForm(request.POST or None, initial=initial_dict)
    warning_d = warning_s = False
    if request.method == 'POST':
        if 'save' in request.POST:
            if form.is_valid():
                if form.cleaned_data['deadline'] is None:
                    warning_d = True
                if form.cleaned_data['subject'] == "":
                    warning_s = True
                if warning_d or warning_s:
                    return render(request, 'jikanwari/edit_assignment.html', {'form': form, 'warning_d': warning_d, 'warning_s': warning_s})
                else:
                    Assignments.objects.filter(pk=pk).delete()

                    Assignments.objects.create(
                        deadline = form.cleaned_data['deadline'],
                        subject = form.cleaned_data['subject'], 
                        memo = form.cleaned_data['memo'], 
                        color = form.cleaned_data['color'],
                        label = form.cleaned_data['label'],
                    )
                    return redirect('assignments')
    return render(request, 'jikanwari/edit_assignment.html', {'form': form, 'warning_d': warning_d, 'warning_s': warning_s})


def register_assignment(request):
    form = AssignmentForm(request.POST or None)
    warning_d = warning_s = False
    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['deadline'] is None:
                warning_d = True
            if form.cleaned_data['subject'] == "":
                warning_s = True
            if warning_d or warning_s:
                return render(request, 'jikanwari/register_assignment.html', {'form': form, 'warning_d': warning_d, 'warning_s': warning_s})
            else:
                Assignments.objects.create(
                    deadline = form.cleaned_data['deadline'],
                    subject = form.cleaned_data['subject'], 
                    memo = form.cleaned_data['memo'], 
                    color = form.cleaned_data['color'],
                    label = form.cleaned_data['label'],
                )
                return redirect('assignments')
    return render(request, 'jikanwari/register_assignment.html', {'form': form, 'warning_d': warning_d, 'warning_s': warning_s})


def register_assignments(request):
    form = AssignmentsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            date = form.cleaned_data['start']
            day = form.cleaned_data['day']
            date_i = next_weekday(date, day)
            time = form.cleaned_data['time']
            dt = get_dt(date_i, time)
            for i in range(form.cleaned_data['number']):
                Assignments.objects.create(
                    subject = form.cleaned_data['subject'], 
                    memo = form.cleaned_data['memo'], 
                    color = form.cleaned_data['color'],
                    label = form.cleaned_data['label'],
                    deadline = dt + timedelta(days=i*7)
                )
            return redirect('assignments')
    return render(request, 'jikanwari/register_assignments.html', {'form': form})


def next_weekday(d, weekday):
    days_ahead = int(weekday) - d.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return d + timedelta(days_ahead)


def get_dt(date, time):
    date = date.strftime("%Y/%m/%d")
    time = time.strftime("%H:%M")
    date_str = date + ' ' + time
    return datetime.strptime(date_str, '%Y/%m/%d %H:%M')


def delete(request, pk):
    Assignments.objects.filter(pk=pk).delete()    
    obj = Assignments.objects.order_by('deadline')
    check = False
    if not obj.exists():
        check = True
    dic = {'obj': obj, 'check': check}
    return render(request, 'jikanwari/assignments.html', dic)


#get day_period of Class and open the link
def webbrowser_open(s):
    c = Class.objects.get(day_period=s)
    link = c.url
    webbrowser.open(link)


def short_to_long(short):
    dic = {
        'Mon': 'monday',
        'Tue': 'tuesday',
        'Wed': 'wednesday',
        'Thu': 'thursday',
        'Fri': 'friday',
        'Sat': 'saturday',
        'Sun': 'sunday'
    }
    return dic[short]


#variable to stop open_link
stop = False


#function to make a reservation of opening the links of all classes
def open_link():
    setting = Settings.objects.get()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    periods = ['1', '2', '3', '4', '5', '6', '7']
    str1 = 'setting.sN'
    str2 = 'schedule.every().weekday.at(time).do(webbrowser_open, dp)'
    for day in days:
        for period in periods:
            str1_modified = str1.replace('N', period)
            time = eval(str1_modified)
            if time != None:
                str_time = (datetime.combine(date.today(), time) - timedelta(minutes=1)).strftime('%H:%M')
                str2_modified = str2.replace('weekday', short_to_long(day)).replace('time', '"'+str_time+'"').replace('dp', '"'+day+period+'"')
                eval(str2_modified)
    while True:
        if stop == True:
            return
        schedule.run_pending()
        tm.sleep(60)
