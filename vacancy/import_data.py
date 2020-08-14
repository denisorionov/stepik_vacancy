from vacancy.data import companies, specialties, jobs
from vacancy.models import Company, Specialty, Vacancy


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
