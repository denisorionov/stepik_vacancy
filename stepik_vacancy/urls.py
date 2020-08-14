from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancy.views import MainView, custom_handler404, custom_handler500, VacanciesView, SpecializationView, \
    CompanyView, VacancyView, VacanciesSendView, MyVacanciesView, MyVacancy, MySignupView, login, logout, \
    MyResumeView, MyResumeCreate, CompanyEdit, MyCompanyView, MyVacanciesCreateView, NewVacancyView

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),
    path('vacancies/', VacanciesView.as_view()),
    path('vacancies/cat/<str:specialization>/', SpecializationView.as_view()),
    path('companies/<int:id>/', CompanyView.as_view()),
    path('vacancies/<int:id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:id>/send/', VacanciesSendView.as_view(), name='vacancy_send'),
    path('mycompany/', MyCompanyView.as_view()),
    path('mycompany/edit/', CompanyEdit.as_view(), name='company_edit'),
    path('mycompany/vacancies/', MyVacanciesView.as_view()),
    path('mycompany/vacancies/create/', MyVacanciesCreateView.as_view()),
    path('mycompany/vacancies/create/new', NewVacancyView.as_view()),
    path('mycompany/vacancies/<int:id>', MyVacancy.as_view(), name='my_vacancy_edit'),
    path('signup/', MySignupView.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myresume/', MyResumeView.as_view()),
    path('myresume/create/', MyResumeCreate.as_view(), name='my_resume_create')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
