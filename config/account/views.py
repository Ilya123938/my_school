from django.shortcuts import render,redirect
from .models import Account,Teacher,Student,Grade

from .forms import RegisterForm,CreateStudentForm,CreateRecordForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'account/home.html')
    
@login_required(login_url='accounts:login')
def redirect_user(request):
    if request.user.role == 'TR':
        return redirect('accounts:teacher_dashboard')
    elif request.user.role == 'ST':
        return redirect('accounts:students_dashboard')
    else:
        return redirect('accounts:login')
    
@login_required(login_url='accounts:login')   
def teacher_dashboard(request):
    if request.user.role != 'TR':
        return redirect('accounts:login')

    teacher =request.user.teacher_profile
    students = teacher.students.all().prefetch_related('grades')

    context = {
        'teacher': teacher,
        'students': students,
        'students_count': students.count(),
    }
    return render(request,'account/teacher_dashboard.html',context)


@login_required(login_url='accounts:login') 
def student_dashboard(request):
    if request.user.role != 'ST':
        return redirect('accounts:login') 
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('accounts:login')  # أو صفحة خطأ
    teacher = student.teacher          # ✅ تعريف الأستاذ
    subject = teacher.subject if teacher else None

   

    grades = student.grades.all()  # كل النتائج الخاصة بالطالب

  
    
    context = {
        'student': student,
        'teacher': teacher,
        'grades': grades,
        'subject' : subject,
       

    } 
    return render(request,'account/students_dashboard.html',context)
    




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            country = form.cleaned_data['country']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']  

            user = Account.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                country=country,
                password=password,
                role=role     
            )

            
            if role == 'TR':
                Teacher.objects.create(user=user)
            elif role == 'ST':
                Student.objects.create(user=user)

            return redirect('accounts:login')
    else:
        form = RegisterForm()
    
    return render(request, 'account/register.html', {'form': form})



def my_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            
            return redirect('accounts:redirect_user')
        
    
        else:
            return redirect('accounts:login')
    
    return render(request,'account/login.html')
@login_required(login_url='accounts:login')
def log_out(request):
    logout(request)
    return redirect('accounts:login')



@login_required
def create_record(request):
    if request.user.role != 'TR':
        return redirect('accounts:login')

    teacher = request.user.teacher_profile

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.subject = teacher.subject

            # 🔒 تحقق هل النتيجة مسجلة مسبقًا
            exists = Grade.objects.filter(
                student=grade.student,
                subject=grade.subject
            ).exists()

            if exists:
                form.add_error(None, 'تم تسجيل نتيجة هذا الطالب لهذه المادة مسبقًا')
            else:
                
                grade.save()
                return redirect('accounts:teacher_dashboard')
    else:
        form = CreateRecordForm()

    return render(request, 'account/create_records.html', {'form': form})


        


@login_required(login_url='accounts:login') 
def create_student(request):
    # فقط المعلم يمكنه إضافة الطلاب
    if request.user.role != 'TR':
        return redirect('accounts:login')

    teacher = request.user.teacher_profile  # Teacher profile

    if request.method == 'POST':
        form = CreateStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)

            # ربط الطالب بالأستاذ
            student.teacher = teacher
            student.save()

            # ✅ ربط الطالب بمادة الأستاذ (ManyToMany)
            if teacher.subject:
                student.subjects.add(teacher.subject)

            return redirect('accounts:teacher_dashboard')
    else:
        form = CreateStudentForm()
    
    return render(request, 'account/create_student.html', {'form': form})


@login_required
def edit_grade(request, grade_id):
    if request.user.role != 'TR':
        return redirect('accounts:login')

    teacher = request.user.teacher_profile
    grade = Grade.objects.get(id=grade_id)

    # 🔒 حماية: لا يمكن تعديل نتيجة لطالب ليس تابعًا لهذا الأستاذ
    if grade.student.teacher != teacher:
        return redirect('accounts:teacher_dashboard')

    if request.method == 'POST':
        form = CreateRecordForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('accounts:teacher_dashboard')
    else:
        form = CreateRecordForm(instance=grade)

    return render(request, 'account/edit_grade.html', {
        'form': form,
        'grade': grade
    })



@login_required
def delete_grade(request, grade_id):
    if request.user.role != 'TR':
        return redirect('accounts:login')

    teacher = request.user.teacher_profile
    grade = Grade.objects.get(id=grade_id)

    # 🔒 حماية
    if grade.student.teacher != teacher:
        return redirect('accounts:teacher_dashboard')

    if request.method == 'POST':
        grade.delete()
        return redirect('accounts:teacher_dashboard')

    return render(request, 'account/delete_grade.html', {
        'grade': grade
    })



        






