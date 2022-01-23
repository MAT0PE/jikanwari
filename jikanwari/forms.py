from django import forms
from .models import Class

COLOR_CHOICES = (
    ('#FFFFFF', '白'),
    ('#1E90FF', '青'),
    ('#FF4500', '赤'),
    ('#32CD32', '緑'),
    ('#FFFF4A', '黄色'),
)

class ClassForm(forms.Form):
    name = forms.CharField(label='授業名', max_length=20, required=False, widget=forms.Textarea(attrs={'cols': '25', 'rows': '1'}))
    url = forms.URLField(label='URL', required=False, help_text='　例）zoomのリンク', widget=forms.Textarea(attrs={'cols': '60', 'rows': '3'}))
    memo = forms.CharField(label='メモ', required=False, help_text='　例）教室の名前', widget=forms.Textarea(attrs={'cols': '60', 'rows': '2'}))
    color = forms.ChoiceField(label='色', widget=forms.Select, choices=COLOR_CHOICES, required=True)

PERIOD_CHOICES = (
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
)

class SettingsForm(forms.Form):
    sat = forms.BooleanField(label='土曜日も表示する', required=False)
    sun = forms.BooleanField(label='日曜日も表示する', required=False)
    open_link = forms.BooleanField(label='時間になったらリンクを開く', required=False)
    s1 = forms.TimeField(required=False, input_formats=['%H:%M'], help_text='　例）9:00 〜 10:30')
    e1 = forms.TimeField(required=False, input_formats=['%H:%M'])
    s2 = forms.TimeField(required=False, input_formats=['%H:%M'])
    e2 = forms.TimeField(required=False, input_formats=['%H:%M'])
    s3 = forms.TimeField(required=False, input_formats=['%H:%M'])
    e3 = forms.TimeField(required=False, input_formats=['%H:%M'])
    s4 = forms.TimeField(required=False, input_formats=['%H:%M'])
    e4 = forms.TimeField(required=False, input_formats=['%H:%M'])
    s5 = forms.TimeField(required=False, input_formats=['%H:%M'])
    e5 = forms.TimeField(required=False, input_formats=['%H:%M'])
    s6 = forms.TimeField(required=False, input_formats=['%H:%M'])
    e6 = forms.TimeField(required=False, input_formats=['%H:%M'])
    s7 = forms.TimeField(required=False, input_formats=['%H:%M'])
    e7 = forms.TimeField(required=False, input_formats=['%H:%M'])
    period = forms.ChoiceField(label='表示する最終時限', required=True, widget=forms.Select, choices=PERIOD_CHOICES)

# PERIOD_CHOICES2 = (
#     ('1', '1'),
#     ('2', '2'),
#     ('3', '3'),
#     ('4', '4'),
#     ('5', '5'),
#     ('6', '6'),
#     ('7', '7'),
# )

LABEL_CHOICES = (
    ('レポート', 'レポート'),
    ('テスト', 'テスト'),
    ('その他', 'その他'),
)

classes = Class.objects.all()
class_names = []
if Class.objects.exists():
    for c in classes:
        if c.name not in class_names:
            class_names.append(c.name)
SUBJECT_CHOICES = []
for class_name in class_names:
    SUBJECT_CHOICES.append((class_name, class_name))

class AssignmentForm(forms.Form):
    deadline = forms.DateTimeField(label='期限', required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), input_formats=['%Y-%m-%dT%H:%M'], help_text='　この項目は必須です')
    # day = forms.ChoiceField(label='曜日', widget=forms.Select, required=False, choices=DAY_CHOICES)
    # period = forms.ChoiceField(label='時限', widget=forms.Select, required=False, choices=PERIOD_CHOICES2)
    subject = forms.ChoiceField(label='授業名', required=False, widget=forms.Select, choices=SUBJECT_CHOICES, help_text='　この項目は必須です')
    memo = forms.CharField(label='メモ', required=False)
    color = forms.ChoiceField(label='色', widget=forms.Select, choices=COLOR_CHOICES, required=True)
    label = forms.ChoiceField(label='種類', widget=forms.Select, choices=LABEL_CHOICES,  required=True)

DAY_CHOICES = (
    (0, '月'),
    (1, '火'),
    (2, '水'),
    (3, '木'),
    (4, '金'),
    (5, '土'),
    (6, '日'),
)

class AssignmentsForm(forms.Form):
    subject = forms.CharField(label='授業名', required=True, widget=forms.Textarea(attrs={'cols': '25', 'rows': '1'}))
    memo = forms.CharField(label='メモ', required=False, widget=forms.Textarea(attrs={'cols': '60', 'rows': '2'}))
    color = forms.ChoiceField(label='色', widget=forms.Select, choices=COLOR_CHOICES, required=True)
    label = forms.ChoiceField(label='種類', widget=forms.Select, choices=LABEL_CHOICES,  required=True)
    day = forms.ChoiceField(label='提出曜日', required=True, widget=forms.Select, choices=DAY_CHOICES)
    time = forms.TimeField(label='提出時刻', required=True, widget=forms.TimeInput(attrs={"type": "time-local"}), input_formats=['%H:%M'], help_text='　例）20:00')
    start = forms.DateField(label='開始日', required=True, widget=forms.DateInput(attrs={"type": "date"}), input_formats=['%Y-%m-%d'], help_text='　この日付以降で最初に上の曜日になる日を初日として課題を登録します')
    number = forms.IntegerField(label='まとめて登録する課題の数', required=True)
