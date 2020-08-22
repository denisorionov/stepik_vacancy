from django.contrib.auth.models import User
from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='picture', height_field='height_field',
                                width_field='width_field', default=None, null=True, )
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url


class Company(models.Model):
    name = models.CharField(max_length=80, default=None, null=True, blank=True)
    title = models.CharField(max_length=64)
    location = models.CharField(max_length=64, default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    employee_count = models.TextField(default=None, null=True, blank=True)
    test = models.TextField(default=None, null=True, blank=True)
    logo = models.ImageField(upload_to='logo', height_field='height_field', width_field='width_field',
                             default=None, null=True, blank=True)
    height_field = models.PositiveIntegerField(default=0, null=True)
    width_field = models.PositiveIntegerField(default=0, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', default=None, null=True, blank=True)

    @property  # для отображения вакансий у компаний которых нет logo; в шаблоне: object.logo_url|default_if_none:'#'
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url


class Vacancy(models.Model):
    title = models.CharField(max_length=64, default=None, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField(default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    salary_min = models.CharField(max_length=7)
    salary_max = models.CharField(max_length=8)
    published_at = models.CharField(max_length=30)


class Application(models.Model):
    written_username = models.CharField(max_length=30)
    written_phone = models.CharField(max_length=12)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    status = models.CharField(max_length=30)
    salary = models.CharField(max_length=8)
    specialty = models.CharField(max_length=64)
    grade = models.CharField(max_length=64)
    education = models.CharField(max_length=64)
    experience = models.CharField(max_length=64)
    portfolio = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_owner', default=None, null=True,
                              blank=True)
