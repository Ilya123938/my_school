from django.contrib import admin
from .models import Account,Subject,Student,Teacher,Grade
# Register your models here.
admin.site.register(Account)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Grade)


