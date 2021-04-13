from django import forms

from vacancies.models import Vacancy, Company, Application, Resume


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('owner',)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': 'Ваше имя',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',

        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('company', 'published_at')


class ResumeForm(forms.ModelForm):
    class Meta:
        GRADE_CHOICE = [
            ('lead', 'Лид'),
            ('senior', 'Синьор'),
            ('middle', 'Мидл'),
            ('junior', 'Джуниор'),
            ('intern', 'Стажер')
        ]
        STATUS_CHOICE = [
            ('in_the_search', 'Ищу работу'),
            ('consider_offers', 'Рассматриваю предложения'),
            ('not_in_the_search', 'Не ищу работу')
        ]
        SPECIALTY_CHOICE = [
            ('frontend', 'Фронтенд-разработчик'),
            ('backend', 'Бекенд-Разработчик'),
            ('fullstack', 'Фулстек-разработчик'),
            ('gamedev', 'Геймдев'),
            ('devops', 'Девопс'),
            ('design', 'Дизайн'),
            ('products', 'Продукты'),
            ('management', 'Менеджмент'),
            ('testing', 'Тестирование'),

        ]
        model = Resume
        fields = ['name', 'surname', 'status', 'grade', 'experience', 'salary', 'specialty', 'education', 'portfolio', ]
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'surname': forms.TextInput(attrs={"class": "form-control"}),
            'status': forms.Select(choices=STATUS_CHOICE,
                                   attrs={"class": "form-control"}),
            'grade': forms.Select(choices=GRADE_CHOICE,
                                  attrs={"class": "form-control"}),
            'experience': forms.Textarea(attrs={"class": "form-control",
                                                "style": "color:#000",
                                                "rows": 4
                                                }),
            'salary': forms.TextInput(attrs={"class": "form-control"}),
            'specialty': forms.Select(choices=SPECIALTY_CHOICE,
                                      attrs={"class": "form-control"}),
            'education': forms.Textarea(attrs={"class": "form-control",
                                               "style": "color:#000",
                                               "rows": 4
                                               }),
            'portfolio': forms.URLInput(attrs={"placeholder": "http://anylink.github.io",
                                               "style": "color:#000",
                                               "class": "form-control"}),
        }