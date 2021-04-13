from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from phone_field import PhoneField


class Specialty(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='images/pics/')
    pass

    class Meta:
        verbose_name_plural = 'Specialties'

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='images/logo/')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, null=True, on_delete=models.PROTECT, related_name='company')

    class Meta:
        verbose_name_plural = 'Companies'

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=15)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.CASCADE)
    skills = models.CharField(max_length=225)
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=20, decimal_places=2)
    salary_max = models.DecimalField(max_digits=20, decimal_places=2)
    published_at = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.salary_min > self.salary_max:
            raise ValidationError({
                'salary_min': ValidationError('"salary_min" must be less than "salary_max"'),
                'salary_max': ValidationError('"salary_min" must be less than "salary_max"')
            })


class Application(models.Model):
    written_username = models.CharField(max_length=30)
    written_phone = PhoneField(blank=True, help_text='Contact phone number')
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)


class Resume(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT, related_name='resume')
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    status = models.CharField(max_length=30)
    salary = models.PositiveIntegerField()
    specialty = models.CharField(max_length=50)
    education = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    experience = models.TextField()
    portfolio = models.URLField()

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

