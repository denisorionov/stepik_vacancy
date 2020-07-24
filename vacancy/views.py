from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View

from vacancy.models import Specialty, Company, Vacancy
from .some_def import declension


class MainView(View):
    def get(self, request, *args, **kwargs):
        vacancy_qt = list()
        company_qt = list()
        specialty = Specialty.objects.values()
        companies = Company.objects.values()

        for special in specialty:
            vacancy_qt.append({
                'title': special['title'],
                'quantity': declension(Vacancy.objects.filter(specialty__code=special['code']).count()),
                'picture': special['picture'],
                'code': special['code']
            })

        for company in companies:
            company_qt.append({
                'logo': company['logo'],
                'quantity': declension(Vacancy.objects.filter(company__title=company['title']).count()),
                'id': company['id']
            })

        return render(request, 'index.html', context={'vacancy_qt': vacancy_qt, 'company_qt': company_qt})


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.values()
        vacan = list()

        for vacancy in vacancies:
            vacan.append({
                'code': Vacancy.objects.get(id=vacancy['id']).specialty.title,
                'logo': Vacancy.objects.get(id=vacancy['id']).company.logo,
                'vacancy': vacancy,
                'id': vacancy['id']
            })
        vacancies_qt = declension(Vacancy.objects.all().count())

        return render(request, 'vacancy/all_vacancies.html', context={'vacan': vacan, 'vacancies_qt': vacancies_qt})


class SpecializationView(View):
    def get(self, request, specialization, *args, **kwargs):
        vacancies = Vacancy.objects.filter(specialty__code=specialization)
        speciality_inf = {'qt': declension(vacancies.all().count()),
                          'logo': Specialty.objects.get(code=specialization).picture,
                          'name': Specialty.objects.get(code=specialization).title,
                          }

        return render(request, 'vacancy/vacancies.html', context={'vacancies': vacancies,
                                                                  'speciality_inf': speciality_inf})


class CompanyView(View):
    def get(self, request, id, *args, **kwargs):
        identify = list()
        vacancies = Vacancy.objects.filter(company__id=id)

        for company in Company.objects.values():
            identify.append(company['id'])

        if id not in identify:
            raise Http404

        company_inf = {'qt': declension(vacancies.all().count()),
                       'logo': Company.objects.get(id=id).logo,
                       'name': Company.objects.get(id=id).name}

        return render(request, 'vacancy/company.html', context={'vacancies': vacancies, 'company_inf': company_inf})


class VacancyView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy_id = Vacancy.objects.values()
        id_list = list()

        for v in vacancy_id:
            id_list.append(v['id'])

        if id not in id_list:
            raise Http404

        vacancy = Vacancy.objects.get(id=id)
        inf = {
            'logo': Vacancy.objects.get(id=id).company.logo,
            'code': Vacancy.objects.get(id=id).specialty.title,
            'company_id': Vacancy.objects.get(id=id).company.id
        }

        return render(request, 'vacancy/vacancy.html', context={'vacancy': vacancy, 'inf': inf})


def custom_handler404(request, exception):
    return HttpResponseNotFound("<h1>Ошибка! Скоро починим!</h1>")


def custom_handler500(request):
    return HttpResponseServerError("<h1>Ошибка! Скоро починим!</h1>")
