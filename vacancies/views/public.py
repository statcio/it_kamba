from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView, ListView

from vacancies.forms import ApplicationForm
from vacancies.models import Vacancy, Company, Specialty


class CompanyView(TemplateView):
    template_name = 'company.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data()
        company = get_object_or_404(Company, id=id)
        context['vacancies'] = Vacancy.objects.filter(company=company).select_related('company', 'specialty')
        context['companies'] = Company.objects.all
        return context


class DetailVacancyView(TemplateView):
    form_class = ApplicationForm
    template_name = 'vacancy.html'

    def get_context_data(self, vacancy_id, **kwargs):
        context = super().get_context_data()
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        context['vacancy'] = vacancy
        context['application_form'] = ApplicationForm()
        return context

    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        application_form = self.form_class(request.POST)

        if not application_form.is_valid():
            return render(request, self.template_name, {
                'vacancy': vacancy,
                'application_form': application_form
            })
        if not request.user.is_authenticated:
            messages.error(request, 'Отклик могут оставить только авторизованные.')
            return render(request, self.template_name, {
                'vacancy': vacancy,
                'application_form': application_form,
            })

        application = application_form.save(commit=False)
        application.vacancy_id = vacancy_id
        application.user = request.user
        application.save()
        messages.info(request, 'Ваш отклик отправлен')
        return render(request, 'sent.html')


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data()

        context['companies'] = Company.objects.all()
        context['specialties'] = Specialty.objects.all()
        context['vacancies'] = Vacancy.objects.all()
        context['keywords'] = ['Python', 'Flask', 'Django', 'DevOps', 'ML']
        return context


class VacancyView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data()
        context['companies'] = Company.objects.all()
        context['vacancies'] = Vacancy.objects.all()
        return context


class VacancyCatView(TemplateView):
    template_name = 'vacancy_cat.html'

    def get_context_data(self, specialty_code, **kwargs):
        context = super().get_context_data()
        specialty = get_object_or_404(Specialty, code=specialty_code)
        context['vacancies'] = Vacancy.objects.filter(specialty=specialty).select_related('company', 'specialty')
        context['title'] = specialty.title
        return context


class CompaniesView(TemplateView):
    template_name = 'companies.html'

    def get_context_data(self, **kwargs):
        context = super(CompaniesView, self).get_context_data()
        context['companies'] = Company.objects.all()
        return context


class AboutView(View):
    def get(self, request):
        return render(request, "about.html")


class SearchResultsView(ListView):
    def get(self, request):
        search_query = request.GET.get('s')
        if search_query:
            vacancies = Vacancy.objects.filter(Q(title__icontains=search_query) |
                                               Q(skills__icontains=search_query) |
                                               Q(specialty_id__code__icontains=search_query) |
                                               Q(description__icontains=search_query))
        else:
            vacancies = Vacancy.objects.all()

        context = {'vacancies': vacancies}
        return render(request, "search.html", context=context)


def custom_handler500(request):
    return HttpResponseServerError('Внутреняя ошибка сервера')