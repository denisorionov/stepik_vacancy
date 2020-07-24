from django.contrib import admin
from django.urls import path

from vacancy.views import MainView, VacancyView, SpecializationView, CompanyView, VacanciesView
from vacancy.views import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('vacancies/', VacanciesView.as_view()),
    path('vacancies/cat/<str:specialization>/', SpecializationView.as_view()),
    path('companies/<int:id>/', CompanyView.as_view()),
    path('vacancies/<int:id>/', VacancyView.as_view()),
]
