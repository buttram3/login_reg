from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Appointment
import datetime

# Create your views here.
def index(request):
        return render(request, "login_reg_app/index.html")


def registration(request):
    result = User.objects.validateReg(request)

    if result[0] == False:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
        return render(request, "login_reg_app/index.html")

    return log_user_in(request, result[1])

def success(request):
    if not 'user' in request.session:
        return render(request, 'login_reg_app/index.html')
    return render(request, 'login_reg_app/success.html')

def login(request):
    result = User.objects.validateLogin(request)

    if result[0] == False:
        messages.add_message(request, messages.INFO, "Email/password don't match.")
        return render(request, "login_reg_app/index.html")

    return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return render(request, 'login_reg_app/success.html')

def logout(request):
    del request.session['user']
    return render(request, 'login_reg_app/index.html')

def appointments(request):
    if 'user' in request.session:
        today =datetime.date.today()
        user_list = User.objects.filter(id=(request.session['user']['id']))
        current_task_list = Appointment.objects.filter(user=user_list[0]).filter(date = today).order_by('updated_at')
        future_task_list = Appointment.objects.filter(user=user_list[0]).filter(date__gt= today).order_by('created_at')
        if user_list:
            context = {
                'user': user_list[0],
                'currenttasks' :current_task_list,
                'futuretasks' : future_task_list,
                'today': today,
            }
            return render(request, 'login_reg_app/success.html', context)
    return redirect('/')

def add_appointment(request):
    task = request.POST['task']
    date = request.POST['date']
    time = request.POST['time']
    user = User.objects.filter(id = (request.session['user']['id']))[0]
    new_app = Appointment.objects.validate_addapp(task, date, time, user)
    print 'new task!!!!!!!!!!!!!!!!!!!!!'

    if not new_app[0]:
        error_list = new_app[1]
        print error_list
        for error in error_list:
            messages.add_message(request, messages.INFO, error)
    return redirect('/appointments')


def delete_appointment(request, task_id):
    Appointment.objects.filter(id = task_id).delete()
    return redirect('/appointments')

def edit_appointment(request):
    pass
