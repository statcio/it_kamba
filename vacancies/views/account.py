from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from vacancies import models
from vacancies.forms import CompanyForm, VacancyForm, ResumeForm
from vacancies.models import Company, Resume, Vacancy


@method_decorator(login_required, name='dispatch')
class MyResumeView(View):
    def get(self, request):
        if not Resume.objects.filter(user__id=request.user.id).exists():
            return render(request, 'resume-create.html')
        resume = Resume.objects.get(user__id=request.user.id)
        context = {
            'form': ResumeForm(instance=resume),
        }
        return render(request, 'resume-edit.html', context)

    def post(self, request):
        resume = Resume.objects.get(user__id=request.user.id)
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Резюме обновлено')
            return redirect('myresume')
        return render(request, 'resume-edit.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class MyResumeCreate(View):
    def get(self, request):
        if Resume.objects.filter(user__id=request.user.id).exists():
            return redirect('myresume')
        context = {
            'form': ResumeForm,
        }
        messages.add_message(request, messages.INFO, 'Создание нового резюме')
        return render(request, 'resume-edit.html', context)

    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = User.objects.get(id=request.user.id)
            resume.save()
            messages.add_message(request, messages.INFO, 'Резюме создано')
            return redirect('myresume')
        return render(request, 'resume-edit.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class MyCompanyView(View):
    def get(self, request):
        if not Company.objects.filter(owner_id=request.user.id).exists():
            return render(request, 'company/company-create.html')
        company = Company.objects.get(owner_id=request.user.id)
        context = {
            'form': CompanyForm(instance=company),
        }
        return render(request, 'company/company-edit.html', context)

    def post(self, request):
        instance = Company.objects.get(owner_id=request.user.id)
        form = CompanyForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Информация о компании обновлена')
            return redirect('mycompany')
        return render(request, 'company/company-edit.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class MyCompanyCreateView(View):
    def get(self, request):
        if Company.objects.filter(owner_id=request.user.id).exists():
            return redirect('mycompany')
        context = {
            'form': CompanyForm,
        }
        messages.add_message(request, messages.INFO, 'Создание новой компании')
        return render(request, 'company/company-edit.html', context)

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = User.objects.get(id=request.user.id)
            company.save()
            messages.add_message(request, messages.INFO, 'Компания успешно создана')
            return redirect('mycompany')
        return render(request, 'company/company-edit.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class MyCompanyVacancies(View):
    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user).first()
        vacancies = company.vacancies.annotate(count=Count('applications')) \
            .all()
        if len(vacancies) == 0:
            return render(
                request,
                'company/vacancy-list.html',
                context={
                    'title': 'У вас пока нет вакансий,'
                             ' но вы можете создать первую!',
                    'number_vacancies': len(vacancies),
                }
            )
        else:
            return render(
                request,
                'company/vacancy-list.html',
                context={
                    'companies': company,
                    'vacancies': vacancies,
                    'title': '',
                    'number_vacancies': len(vacancies),
                }
            )


@method_decorator(login_required, name='dispatch')
class MyVacanciesСreateView(View):
    def get(self, request, *args, **kwargs):
        vacancy_form = VacancyForm()
        return render(
            request,
            'company/vacancy-edit.html',
            context={
                'title': 'Создайте карточку вакансии',
                'vacancy_form': vacancy_form,
            }
        )

    def post(self, request, *args, **kwargs):
        my_company_vac = models.Company.objects.filter(owner=request.user)
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            vacancy.company = my_company_vac.first()
            vacancy.save()
            return redirect(
                request.path,
                context={
                    'title': 'Вакансия создана'
                }
            )
        else:
            return render(
                request, 'vacancy-edit.html',
                context={
                    'title': 'Создайте вакансию',
                    'vacancy_form': vacancy_form
                }
            )


@method_decorator(login_required, name='dispatch')
class MyVacancyEditView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy = Vacancy.objects.filter(id=id).first()
        if not vacancy:
            raise Http404
        applications = vacancy.applications.all()
        return render(
            request,
            'company/vacancy-edit.html',
            context={
                'vacancy_form': VacancyForm(instance=vacancy),
                'title': 'Хотите отредактировать вакансию?',
                'applications': applications,
                'number_applications': len(applications),
            }
        )

    def post(self, request, id, *args, **kwargs):
        my_company_vac = models.Company.objects.filter(owner=request.user)
        vacancy = models.Vacancy.objects.filter(
            id=id, company=my_company_vac.first()) \
            .first()
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy_form = VacancyForm(request.POST,
                                       request.FILES,
                                       instance=vacancy)
            vacancy_form.save()
            return HttpResponseRedirect(request.path, )
        else:
            return render(
                request, 'vacancy-edit.html',
                context={'title': 'Отредактируйте вакансию',
                         'vacancy_form': vacancy_form
                         }
            )