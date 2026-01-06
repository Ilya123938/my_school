from django.db import models
import pycountry
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


# Create your models here.


countries = list(pycountry.countries)
COUNTRY_CHOICES = [(country.alpha_2,country.name)for country in countries]
    


class AccountManager(BaseUserManager):
    def create_user(self,username,first_name,last_name,email,country,role='ST',password=None):
        if not email:
            raise ValueError('user most have email')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            country = country,
            role =role

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,first_name,last_name,email,country,password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            role='TR',
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('TR', 'Teacher'),
        ('ST', 'Student'),
    )

    username = models.CharField('الاسم الكامل', max_length=200, unique=True)
    first_name = models.CharField('الاسم الشخصي', max_length=200)
    last_name = models.CharField('الاسم العائلي', max_length=200)
    email = models.EmailField('البريد الإلكتروني', unique=True)
    country = models.CharField('البلد', max_length=2, choices=COUNTRY_CHOICES)

    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='ST')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country']

    def __str__(self):
        return self.email
    
class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.user.username

    

from django.db import models
from cloudinary.models import CloudinaryField

class Student(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    photo = CloudinaryField('image', blank=True, null=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )

    def __str__(self):
        return self.user.username

    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject'],
                name='unique_grade_per_subject'
            )
        ]

    def __str__(self):
        return f"{self.student.user.first_name} - {self.subject.name} : {self.score}"







   





