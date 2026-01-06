from django import forms
from .models import Account, Student,Grade

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='كلمة السر',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'كلمة السر',
        

    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={

        'class':'form-control',
        'placeholder':'قم بتاكيد كلمة السر'
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','email','country','role','password']

        widgets ={
            'first_name':forms.TextInput(attrs={
                'placeholder':'الاسم الشخصي'
            }),

            'last_name':forms.TextInput(attrs={
                'placeholder':'الاسم العائيلي'
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':'البريد الالكتروني'
            }),
            'country':forms.Select()
        }

        labels={
            'password' : 'كلمة السر',
            'confirm_password' : 'تاكيد كلمة السر'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('كلمتا المرور غير متطابقتان')
        return cleaned_data
    

class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student','score']

    
   
