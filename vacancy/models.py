from django.db import models

from .data import specialties, companies, jobs


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=64)
    picture = models.TextField(default=None, null=True, blank=True)


class Company(models.Model):
    name = models.CharField(max_length=80, default=None, null=True, blank=True)
    title = models.CharField(max_length=64)
    location = models.CharField(max_length=64, default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    employee_count = models.TextField(default=None, null=True, blank=True)
    test = models.TextField(default=None, null=True, blank=True)
    logo = models.CharField(max_length=100, default=None, null=True)


class Vacancy(models.Model):
    title = models.CharField(max_length=64, default=None, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField(default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    salary_min = models.CharField(max_length=7)
    salary_max = models.CharField(max_length=8)
    published_at = models.CharField(max_length=30)


def add_company():
    for company in companies:
        if len(Company.objects.filter(title=company['title'])) == 0:
            Company.objects.create(title=company['title'])
    return


def add_specialty():
    for specialty in specialties:
        if len(Specialty.objects.filter(code=specialty['code'])) == 0:
            Specialty.objects.create(code=specialty['code'], title=specialty['title'])
    return


def add_vacancy():
    for job in jobs:
        job_specialty = Specialty.objects.get(code__exact=job['cat'])
        job_company = Company.objects.get(title__exact=job['company'])
        if len(Vacancy.objects.filter(title=job['title'])) == 0:
            Vacancy.objects.create(
                title=job['title'], specialty=Specialty(id=job_specialty.id), company=Company(id=job_company.id),
                salary_min=job['salary_from'], salary_max=job['salary_to'], published_at=job['posted']
            )
    return
