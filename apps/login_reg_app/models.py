from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

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
        error=[]
        if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
            error.append("The first or last name can't have numbers")
        if len(request.POST['first_name'])<2 or len(request.POST['last_name'])<2:
            error.append("Please input valid names")
        if not EMAIL_REGEX.match(request.POST['email']):
            error.append("Please input a valid email")
        if len(request.POST['password_create'])<8 or request.POST['password_create'] != request.POST['pw_confirm']:
            error.append("Passwords must match and be at least 8 characters.")
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
    pw_hash= models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
