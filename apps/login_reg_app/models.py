from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
import datetime
# from datetime import datetime, date

today = datetime.date.today
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def validateReg(self, request):
        error = self.validate_inputs(request)
        print error

        if len(error) > 0:
            return(False, error)

        pw_hash = bcrypt.hashpw(request.POST['password_create'].encode(), bcrypt.gensalt())

        user = self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email= request.POST['email'], pw_hash=pw_hash)

        return(True, user)



    def validate_inputs(self, request):
        bday = request.POST['bday']
        error=[]
        if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
            error.append("The first or last name can't have numbers")
        if len(request.POST['first_name'])<2 or len(request.POST['last_name'])<2:
            error.append("Please input valid names")
        if not EMAIL_REGEX.match(request.POST['email']):
            error.append("Please input a valid email")
        if len(request.POST['password_create'])<8 or request.POST['password_create'] != request.POST['pw_confirm']:
            error.append("Passwords must match and be at least 8 characters.")
        # if bday == unicode(datetime.today().date()) or bday > unicode(datetime.today().date()):
        #         errors.append('Birthday needs to be in past')
        return error

    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['user_email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            return(False, ["Email/password don't match."])



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class AppointmentManager(models.Manager):
    def validate_addapp(self, task, date, time, user):
        error_list=[]
        truth= True
        if task == "":
            error_list.append('Task field must contain text!')
            truth = False

        if not time:
            error_list.append('Time field must contain a time!')
            truth = False

        if not date:
            error_list.append('Your appointment must have a date!')
            truth = False
        print date
        if date < today:
            error_list.append('Date must be either today or someday in the future')
            truth = False

        if not truth:
            return (False, error_list)

        new_task = Appointment.objects.create(task=task, date=date, time=time, user=user)
        return (True, new_task)

class Appointment(models.Model):
    task = models.CharField(max_length=420)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=420, default='Pending')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = AppointmentManager()
