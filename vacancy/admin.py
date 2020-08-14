from django.contrib import admin

from .models import Specialty, Company, Vacancy

admin.site.register(Specialty)
admin.site.register(Company)
admin.site.register(Vacancy)
