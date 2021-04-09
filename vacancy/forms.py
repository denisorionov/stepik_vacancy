from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from vacancy.models import Company, Resume, Vacancy, Application

STATUS_CHOICES = [('1', 'Ищу работу'), ('2', 'Открыть к предложениям'), ('3', 'Не ищу работу')]
SPECIALTY_CHOICES = [('1', 'Backend разработка'), ('2', 'Frontend разработка'), ('3', 'Project manager')]
GRADE_CHOICES = [('1', 'Средний (middle)'), ('2', 'Младший (junior)'), ('3', 'Старший (senior)')]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=2, max_length=5)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def clean(self):
        if not self.cleaned_data['first_name'].isalpha():
            raise forms.ValidationError({"first_name": "Имя должно содержать только буквы"})
        if not self.cleaned_data['last_name'].isalpha():
            raise forms.ValidationError({'last_name': 'Фамилия должна содержать только буквы'})
        return self.cleaned_data


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'custom-file-input', 'multiple data-min-file-count': '0'}),
            'employee_count': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio',
                  'owner']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'custom-select mr-sm-2'}, choices=STATUS_CHOICES),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'custom-select mr-sm-2'}, choices=SPECIALTY_CHOICES),
            'grade': forms.Select(attrs={'class': 'custom-select mr-sm-2'}, choices=GRADE_CHOICES),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control'}),
            'portfolio': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.HiddenInput()

        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy

        fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'salary_min': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_max': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application

        fields = ['written_username', 'written_phone', 'written_cover_letter']

        widgets = {
            'written_username': forms.TextInput(attrs={'class': 'form-control'}),
            'written_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'written_cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}),
        }
