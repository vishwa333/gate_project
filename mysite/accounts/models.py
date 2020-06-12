from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class my_manager(BaseUserManager):
    def create_user(self,email,fname="",lname="",password=None):
        if not email:
            raise ValueError("users must have a valid email")
        user = self.model(
            email = self.normalize_email(email),
            fname = fname,
            lname = lname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,fname="",lname="",password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
        )
        user.is_admin= True
        user.is_active=True
        user.is_staff = True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class my_user(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name = "email",max_length=60,unique=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name = "date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name = "last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []
    objects  = my_manager()

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perm(self,app_label):
        return True