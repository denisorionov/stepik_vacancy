from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views import View
from django.views.generic import CreateView

from vacancy.models import Specialty, Company, Vacancy, Resume, Application
from .forms import RegisterForm, ResumeForm, CompanyForm, VacancyForm, ApplicationForm
from .utils import check_anonymous


class MainView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('search', ''):
            search = request.GET.get('search', '')
            vacancy = Vacancy.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
            return render(request, 'vacancy/search.html', context={'vacancies': vacancy, 'vacancy': vacancy})
        else:
            vacancy_inf, company_inf = list(), list()
            companies = Company.objects.all()
            specialties = Specialty.objects.all()

            for specialty in specialties:
                vacancy_inf.append({'specialty': specialty,
                                    'quantity': Vacancy.objects.filter(specialty__code=specialty.code).count()})

            for company in companies:
                company_inf.append(
                    {'company': company, 'quantity': Vacancy.objects.filter(company__title=company.title).count()})

            return render(request, 'index.html', context={'vacancy_inf': vacancy_inf, 'company_inf': company_inf,
                                                          'username': check_anonymous(request)})


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()

        return render(request, 'vacancy/all_vacancies.html',
                      context={'vacancies': vacancies, 'username': check_anonymous(request)})


class SpecializationView(View):
    def get(self, request, specialization, *args, **kwargs):
        vacancies = Vacancy.objects.filter(specialty__code=specialization)
        specialty = Specialty.objects.filter(code=specialization)[0]

        return render(request, 'vacancy/vacancies.html', context={'vacancies': vacancies,
                                                                  'specialty': specialty,
                                                                  'username': check_anonymous(request)})


class CompanyView(View):
    def get(self, request, id, *args, **kwargs):
        vacancies = Vacancy.objects.filter(company__id=id)
        company = Company.objects.filter(id=id)[0]

        return render(request, 'vacancy/company.html',
                      context={'vacancies': vacancies, 'company': company, 'username': check_anonymous(request)})


class VacancyView(View):
    def get(self, request, id):
        vacancy = Vacancy.objects.filter(id=id)[0]
        application_form = ApplicationForm()

        return render(request, 'vacancy/vacancy.html', context={'vacancy': vacancy, 'form': application_form,
                                                                'username': check_anonymous(request)})

    def post(self, request, id):
        application_form = ApplicationForm(request.POST)
        vacancy = Vacancy.objects.filter(id=id)[0]
        args = {}

        if vacancy.applications.filter(user_id=request.user.id):
            args['repeat'] = True

            return render(request, 'vacancy/vacancy.html',
                          context={'vacancy': vacancy, 'form': application_form, 'args': args,
                                   'username': check_anonymous(request)})

        else:
            if application_form.is_valid():
                application_form.instance.user = request.user
                application_form.instance.vacancy = Vacancy.objects.get(id=id)
                application_form.save()

                return redirect('vacancy_send', id=id)


class VacanciesSendView(View):
    def get(self, request, id):
        vacancy = Vacancy.objects.get(id=id)

        return render(request, 'vacancy/sent.html', context={'vacancy': vacancy, 'username': check_anonymous(request)})


class MyCompanyView(View):
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)

        for owner_id in Company.objects.values('owner_id'):
            if owner_id['owner_id'] == user.id:
                return redirect('edit/')

        return render(request, 'vacancy/company-create.html', context={'username': check_anonymous(request)})


class CompanyEdit(View):
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        id_list = list()

        for owner_id in Company.objects.values('owner_id'):
            id_list.append(owner_id['owner_id'])

        if user.id in id_list:
            company = Company.objects.get(owner_id=user.id)
            company_form = CompanyForm(instance=company)
        else:
            company = None
            company_form = CompanyForm()

        return render(request, 'vacancy/company-edit.html',
                      context={'form': company_form, 'company': company, 'username': check_anonymous(request)})

    def post(self, request):
        user = auth.get_user(request)
        id_list = list()

        for owner_id in Company.objects.values('owner_id'):
            id_list.append(owner_id['owner_id'])

        if user.id in id_list:
            company = Company.objects.get(owner_id=user.id)
            company_form = CompanyForm(request.POST, request.FILES, instance=company)
            company_form.instance.logo = company.logo
        else:
            company = None
            company_form = CompanyForm(request.POST, request.FILES)

        if company_form.is_valid():
            company_form.save(commit=False)
            company_form.instance.owner = request.user
            company_form.save()

            return redirect('/mycompany/edit/')

        return render(request, 'vacancy/company-edit.html',
                      context={'form': company_form, 'company': company, 'username': check_anonymous(request)})


class MyVacanciesView(View):
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        for company in Company.objects.values('owner_id', 'id'):
            if company['owner_id'] == user.id:
                vacancies = Vacancy.objects.filter(company=company['id'])
        return render(request, 'vacancy/vacancy-list.html',
                      context={'username': check_anonymous(request), 'vacancies': vacancies})


class MyVacanciesCreateView(View):
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)

        if len(User.objects.filter(id=user.id)[0].user.all()) == 0:
            return redirect('/mycompany/edit/')

        if len(Company.objects.filter(owner_id=user.id)[0].vacancies.all()) > 0:
            return redirect('/mycompany/vacancies/')

        return render(request, 'vacancy/vacancy-create.html', context={'username': check_anonymous(request)})


class NewVacancyView(View):
    def get(self, request, *args, **kwargs):
        vacancy_form = VacancyForm()
        return render(request, 'vacancy/vacancy-edit.html',
                      context={'username': check_anonymous(request), 'form': vacancy_form})

    def post(self, request):
        vacancy_form = VacancyForm(request.POST)
        company = Company.objects.filter(owner_id=request.user.id)[0]
        args = {}
        if vacancy_form.is_valid():
            vacancy_form.instance.company = company
            vacancy_form.save()
            args['inf_edit'] = True

            return render(request, 'vacancy/vacancy-edit.html',
                          context={'form': vacancy_form, 'args': args, 'username': check_anonymous(request)})


class MyVacancy(View):
    def get(self, request, id):
        vacancy_form = VacancyForm()
        applications = Application.objects.filter(vacancy_id=id)

        for vacancies in Vacancy.objects.values():
            if vacancies['id'] == id:
                vacancy_form = VacancyForm(instance=Vacancy.objects.get(id=id))

        return render(request, 'vacancy/vacancy-edit.html',
                      context={'username': check_anonymous(request), 'form': vacancy_form,
                               'applications': applications})

    def post(self, request, id):
        user = auth.get_user(request)
        owner_id = User.objects.filter(id=user.id)[0].id
        company = Company.objects.filter(owner__id=owner_id)[0]
        id_list = list()
        args = {}

        for vacancy in Vacancy.objects.values():
            id_list.append(vacancy['id'])

        if id in id_list:
            vacancy = Vacancy.objects.get(id=id)
            vacancy_form = VacancyForm(request.POST, instance=vacancy)
        else:
            vacancy_form = VacancyForm(request.POST)

        if vacancy_form.is_valid():
            vacancy_form.save(commit=False)
            vacancy_form.instance.company = company
            vacancy_form.save()
            args['inf_edit'] = True

            return render(request, 'vacancy/vacancy-edit.html',
                          context={'form': vacancy_form, 'args': args, 'username': check_anonymous(request)})

        return render(request, 'vacancy/vacancy-edit.html',
                      context={'form': vacancy_form, 'username': check_anonymous(request)})


class MyResumeView(View):
    def get(self, request):
        user = auth.get_user(request)
        for owner_id in Resume.objects.values('owner_id'):
            if owner_id['owner_id'] == user.id:
                resume = Resume.objects.get(owner_id=user.id)
                resume_form = ResumeForm(instance=resume)

                return render(request, 'vacancy/resume-edit.html',
                              context={'form': resume_form, 'username': check_anonymous(request)})

        return render(request, 'vacancy/resume-create.html', context={'username': check_anonymous(request)})


class MyResumeCreate(View):
    def get(self, request):
        user = auth.get_user(request)
        id_list = list()

        for owner_id in Resume.objects.values('owner_id'):
            id_list.append(owner_id['owner_id'])

        if user.id in id_list:
            resume = Resume.objects.get(owner_id=user.id)
            resume_form = ResumeForm(instance=resume)
        else:
            resume_form = ResumeForm()

        return render(request, 'vacancy/resume-edit.html',
                      context={'form': resume_form, 'username': check_anonymous(request)})

    def post(self, request):
        user = auth.get_user(request)
        args = {}
        id_list = list()

        for owner_id in Resume.objects.values('owner_id'):
            id_list.append(owner_id['owner_id'])

        if user.id in id_list:
            resume = Resume.objects.get(owner_id=user.id)
            resume_form = ResumeForm(request.POST, instance=resume)
        else:
            resume_form = ResumeForm(request.POST)

        if resume_form.is_valid():
            resume_form.save(commit=False)
            resume_form.instance.owner = request.user
            resume_form.save()
            args['inf_edit'] = True

            return render(request, 'vacancy/resume-edit.html',
                          context={'form': resume_form, 'args': args, 'username': check_anonymous(request)})

        return render(request, 'vacancy/resume-edit.html',
                      context={'form': resume_form, 'username': check_anonymous(request)})


class MySignupView(CreateView):
    form_class = RegisterForm
    success_url = 'login'
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('/login/')


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = 'Пользователь не найден'
            return render(request, 'login.html', context={'args': args})
    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def custom_handler404(request, exception):
    return HttpResponseNotFound("<h1>Ошибка! Скоро починим!</h1>")


def custom_handler500(request):
    return HttpResponseServerError("<h1>Ошибка! Скоро починим!</h1>")
