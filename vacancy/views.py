from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views import View
from django.views.generic import CreateView

from vacancy.models import Specialty, Company, Vacancy, Resume, Application
from .forms import RegisterForm, ResumeForm, CompanyForm, VacancyForm, ApplicationForm


class MainView(View):  # главная страница
    def get(self, request, *args, **kwargs):
        companies = Company.objects.annotate(qt=Count('vacancies'))  # кол-во вакансий для каждой компании
        specialties = Specialty.objects.annotate(qt=Count('vacancies'))  # кол-во вакансий для каждой специализации

        return render(request, 'index.html', context={'companies': companies, 'specialties': specialties})


class SearchView(View):  # страница поиска, поиск по заголовку и описанию вакансии
    def get(self, request, *args, **kwargs):
        if request.GET.get('search', ''):
            search = request.GET.get('search', '')
            vacancy = Vacancy.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
            return render(request, 'vacancy/search.html', context={'vacancies': vacancy, 'vacancy': vacancy})


class VacanciesView(View):  # страница со всеми вакансиями
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()

        return render(request, 'vacancy/all_vacancies.html', context={'vacancies': vacancies})


class SpecializationView(View):  # страница с вакансиями специализации
    def get(self, request, specialization, *args, **kwargs):
        vacancies = Vacancy.objects.filter(specialty__code=specialization)
        specialty = Specialty.objects.filter(code=specialization).first()

        return render(request, 'vacancy/vacancies.html', context={'vacancies': vacancies, 'specialty': specialty})


class CompanyView(View):  # страница с вакансиями компании
    def get(self, request, id):
        vacancies = Vacancy.objects.filter(company__id=id)
        company = Company.objects.filter(id=id).first()

        return render(request, 'vacancy/company.html', context={'vacancies': vacancies, 'company': company})


class VacancyView(View):  # страница вакансии с полем для отправки отклика для авторизованного пользователя
    def get(self, request, id):
        vacancy = Vacancy.objects.filter(id=id).first()
        application_form = ApplicationForm()

        return render(request, 'vacancy/vacancy.html', context={'vacancy': vacancy, 'form': application_form})

    def post(self, request, id):
        application_form = ApplicationForm(request.POST)
        vacancy = Vacancy.objects.filter(id=id).first()
        args = {}

        if vacancy.applications.filter(user_id=request.user.id):
            args['repeat'] = True  # проверка, если пользователь уже откликался, высветится соответствующее сообщение

            return render(request, 'vacancy/vacancy.html',
                          context={'vacancy': vacancy, 'form': application_form, 'args': args})

        else:
            if application_form.is_valid():
                application_form.instance.user = request.user
                application_form.instance.vacancy = Vacancy.objects.get(id=id)
                application_form.save()

                return render(request, 'vacancy/sent.html')


class MyCompanyView(View):  # страница компании пользователя
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)

        if request.user.is_authenticated:
            if Company.objects.filter(owner_id=user.id):
                return redirect('edit/')  # если у пользователя есть компания открывается страница редактирования

            return render(request,
                          'vacancy/company-create.html')  # если у пользователя нет компании, предлагается создать

        else:
            raise Http404  # если пользователь не авторизован - ошибка 404


class CompanyEdit(View):  # страница редактирования компании
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)

        if user.is_authenticated:

            if Company.objects.filter(owner_id=user.id):
                company = Company.objects.get(owner_id=user.id)
                company_form = CompanyForm(instance=company)
            else:
                company = None
                company_form = CompanyForm()

            return render(request, 'vacancy/company-edit.html', context={'form': company_form, 'company': company})

        else:
            raise Http404

    def post(self, request):
        user = auth.get_user(request)

        if Company.objects.filter(owner_id=user.id):
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

        return render(request, 'vacancy/company-edit.html', context={'form': company_form, 'company': company})


class MyVacanciesView(View):  # список вакансий в личном кабинете компании
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if request.user.is_authenticated:
            vacancies = Vacancy.objects.filter(company__owner__id=user.id)
            return render(request, 'vacancy/vacancy-list.html', context={'vacancies': vacancies})
        else:
            raise Http404


class MyVacanciesCreateView(View):  # страница создания/редактирования компании, вакансий
    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)

        if user.is_authenticated:
            # если у пользователя нет компании, при попытке перейти на страницу с вакансиями пользователь
            # перенаправляется на страницу создания/редактирования компании
            if len(User.objects.filter(id=user.id).first().user.all()) == 0:
                return redirect('/mycompany/edit/')

            # если у пользователя есть компания, пользователь может перейти на страницу с вакансиями компании
            elif Company.objects.filter(owner_id=user.id).first().vacancies.all():
                return redirect('/mycompany/vacancies/')

            return render(request, 'vacancy/vacancy-create.html')
        else:
            raise Http404


class NewVacancyView(View):  # страница создания новой вакансии
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            vacancy_form = VacancyForm()
            return render(request, 'vacancy/vacancy-edit.html', context={'form': vacancy_form})
        raise Http404

    def post(self, request):
        vacancy_form = VacancyForm(request.POST)
        company = Company.objects.filter(owner_id=request.user.id).first()
        args = {}
        if vacancy_form.is_valid():
            vacancy_form.instance.company = company
            vacancy_form.save()
            args['inf_edit'] = True

            return render(request, 'vacancy/vacancy-edit.html', context={'form': vacancy_form, 'args': args})


class MyVacancy(View):  # редактирование вакансии компании
    def get(self, request, id):
        applications = Application.objects.filter(vacancy_id=id)
        vacancy_form = VacancyForm(instance=Vacancy.objects.filter(id=id).first())

        if request.user.is_authenticated and Vacancy.objects.filter(company__owner__id=request.user.id).filter(id=id):
            return render(request, 'vacancy/vacancy-edit.html',
                          context={'form': vacancy_form, 'applications': applications})
        else:
            raise Http404  # проверка наличия вакансии у авторизованного пользователя

    def post(self, request, id):
        user = auth.get_user(request)
        company = Company.objects.filter(owner__id=user.id).first()
        args = {}

        if Vacancy.objects.filter(id=id):
            vacancy = Vacancy.objects.filter(id=id).first()
            vacancy_form = VacancyForm(request.POST, instance=vacancy)
        else:
            vacancy_form = VacancyForm(request.POST)

        if vacancy_form.is_valid():
            vacancy_form.save(commit=False)
            vacancy_form.instance.company = company
            vacancy_form.save()
            args['inf_edit'] = True

            return render(request, 'vacancy/vacancy-edit.html',
                          context={'form': vacancy_form, 'args': args})

        return render(request, 'vacancy/vacancy-edit.html', context={'form': vacancy_form})


class MyResumeView(View):  # страница резюме пользователя
    def get(self, request):
        user = auth.get_user(request)
        if user.is_authenticated:
            if Resume.objects.filter(owner_id=user.id):
                resume = Resume.objects.filter(owner_id=user.id).first()
                resume_form = ResumeForm(instance=resume)

                return render(request, 'vacancy/resume-edit.html', context={'form': resume_form})

            return render(request, 'vacancy/resume-create.html')

        raise Http404


class MyResumeCreate(View):  # страница создания/редактирования резюме
    def get(self, request):
        user = auth.get_user(request)
        if user.is_authenticated:
            if Resume.objects.filter(owner_id=user.id):
                resume = Resume.objects.filter(owner_id=user.id).first()
                resume_form = ResumeForm(instance=resume)
            else:
                resume_form = ResumeForm()

            return render(request, 'vacancy/resume-edit.html', context={'form': resume_form})

        raise Http404

    def post(self, request):
        user = auth.get_user(request)
        args = {}

        if Resume.objects.filter(owner_id=user.id):
            resume = Resume.objects.filter(owner_id=user.id).first()
            resume_form = ResumeForm(request.POST, instance=resume)
        else:
            resume_form = ResumeForm(request.POST)

        if resume_form.is_valid():
            resume_form.save(commit=False)
            resume_form.instance.owner = request.user
            resume_form.save()
            args['inf_edit'] = True

            return render(request, 'vacancy/resume-edit.html', context={'form': resume_form, 'args': args})

        return render(request, 'vacancy/resume-edit.html', context={'form': resume_form})


class MySignupView(CreateView):  # регистрация
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
