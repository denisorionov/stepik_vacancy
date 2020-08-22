from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancy.views import MainView, custom_handler404, custom_handler500, VacanciesView, SpecializationView, \
    CompanyView, VacancyView, MyVacanciesView, MyVacancy, MySignupView, login, logout, \
    MyResumeView, MyResumeCreate, CompanyEdit, MyCompanyView, NewVacancyView, SearchView, MyVacanciesCreateView

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),  # главная
    path('search/', SearchView.as_view(), name='search'),  # поиск
    path('vacancies/', VacanciesView.as_view()),  # все вакансии
    path('vacancies/cat/<str:specialization>/', SpecializationView.as_view()),  # вакансии по специализации
    path('companies/<int:id>/', CompanyView.as_view()),  # вакансии компании
    path('vacancies/<int:id>/', VacancyView.as_view(), name='vacancy'),  # вакансия
    path('mycompany/', MyCompanyView.as_view()),  # страница с кнопкой создания компании
    path('mycompany/edit/', CompanyEdit.as_view(), name='company_edit'),  # страница редактирования компании
    path('mycompany/vacancies/', MyVacanciesView.as_view()),  # список вакансий в личном кабинете компании
    path('mycompany/vacancies/create/', MyVacanciesCreateView.as_view()),  # страница с кнопкой создания вакансии
    path('mycompany/vacancies/create/new', NewVacancyView.as_view()),  # страница создания новой вакансии
    path('mycompany/vacancies/<int:id>', MyVacancy.as_view(), name='my_vacancy_edit'),  # редактирование вакансии компании
    path('myresume/', MyResumeView.as_view()),  # страница резюме пользователя
    path('myresume/create/', MyResumeCreate.as_view(), name='my_resume_create'),  # страница создания/редактирования резюме
    path('signup/', MySignupView.as_view(), name='signup'),  # регистрация
    path('login/', login, name='login'),
    path('logout/', logout, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
