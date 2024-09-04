from django.shortcuts import render, redirect, reverse
from .models import Student
from django.contrib import messages

def index(request):
    data = Student.objects.all()  # Fetch all student records
    context = {'data': data}
    return render(request, "index.html", context)

def about(request):
    return render(request, 'about.html')

def insertData(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        if name and email and age and gender:  # Check if all fields are filled
            try:
                student = Student(name=name, email=email, age=age, gender=gender)
                student.save()
                messages.success(request, 'Data inserted successfully.')
                return redirect(reverse('index'))  # Redirect to home page
            except Exception as e:
                messages.error(request, f'Error saving student data: {e}')
                return redirect(reverse('index'))  # Redirect to home page
        else:
            messages.warning(request, 'All fields are required.')
            return redirect(reverse('index'))  # Redirect to home page

    return render(request, 'index.html')

def updateData(request, id):
    try:
        edit = Student.objects.get(id=id)
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect(reverse('index'))  # Redirect to home page

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        gender = request.POST['gender']

        if name and email and age and gender:
            edit.name = name
            edit.email = email
            edit.age = age
            edit.gender = gender
            edit.save()
            messages.success(request, 'Data updated successfully.')
            return redirect(reverse('index'))  # Redirect to home page
        else:
            messages.warning(request, 'All fields are required.')
            return redirect(reverse('index'))  # Redirect to home page

    context = {'d': edit}
    return render(request, "update.html", context)

def deleteData(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        messages.success(request, 'Data deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect(reverse('index'))  # Redirect to home page
