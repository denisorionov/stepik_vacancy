from django.contrib import auth


def declension(n):
    if n == 0 or 20 >= n >= 5 or n >= 12 and n % 10 not in [1, 2, 3, 4]:
        return '{} вакансий'.format(n)
    elif n == 1 or n % 10 == 1 and n != 11:
        return '{} вакансия'.format(n)
    elif n in [2, 3, 4] or n % 10 == 2 or 3 or 4:
        return '{} вакансии'.format(n)


def check_anonymous(request):
    if auth.get_user(request).is_authenticated:
        user = auth.get_user(request)
    else:
        user = False
    return user
