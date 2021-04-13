"""kamba URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from vacancies.views import account
from vacancies.views import authorization
from vacancies.views import public

urlpatterns = [

    path('', public.MainView.as_view(), name='main'),
    path('about/', public.AboutView.as_view(), name='about'),
    path('companies/', public.CompaniesView.as_view(), name='companies'),
    path('vacancies/', public.VacancyView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty_code>/', public.VacancyCatView.as_view(), name='vacancy_by_specialization'),
    path('vacancies/<int:vacancy_id>/', public.DetailVacancyView.as_view(), name='detail_vacancy'),
    path('vacancies/<vacancy_id>/send/', public.DetailVacancyView.as_view()),
    path('companies/<int:id>', public.CompanyView.as_view(), name='company'),
    path('mycompany/', account.MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/create', account.MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/vacancies', account.MyCompanyVacancies.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/create', account.MyVacanciesСreateView.as_view(), name='mycompany_vacancy_create'),
    path('mycompany/vacancies/<int:id>', account.MyVacancyEditView.as_view(), name='mycompany_vacancy'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('login/', authorization.MyLoginView.as_view(), name='login'),
    url('logout/', LogoutView.as_view(), name='logout'),
    path('register/', authorization.MySignupView.as_view(), name='register'),
    path('search/', public.SearchResultsView.as_view(), name='search_results'),
    path('myresume/', account.MyResumeView.as_view(), name='myresume'),
    path('myresume/create', account.MyResumeCreate.as_view(), name='myresume_create'),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)