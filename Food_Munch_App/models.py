from django.db import models
from django.utils import timezone

# Create your models here.

class Video(models.Model):
    Title=models.CharField(max_length=500)
    Video_File=models.FileField(upload_to="videos")
    Upload_DateTime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title

class PaymentSectionDetails(models.Model):
    CustomerName=models.CharField(max_length=50)
    EmailId=models.CharField(max_length=100)
    MobileNumber=models.CharField(max_length=10)
    Address=models.CharField(max_length=100)
    City=models.CharField(max_length=30)
    State=models.CharField(max_length=30)
    PinCode=models.CharField(max_length=6)
    PaymentMethod=models.CharField(max_length=25)
    CardName=models.CharField(max_length=30)
    CardNumber=models.CharField(max_length=19)
    CardExpiry=models.CharField(max_length=7)
    Cvv=models.CharField(max_length=3)
    PaymentDateTime=models.DateTimeField(default=timezone.now)

class SignupSection(models.Model):
    CustomerName=models.CharField(max_length=50)
    MobileNumber=models.CharField(max_length=10,unique=True)
    EmailId=models.CharField(max_length=100,unique=True,default="")
    Password=models.CharField(max_length=50)
    DateOfRegisteration=models.DateTimeField(default=timezone.now)
    UserLastUpdate=models.DateTimeField(auto_now=True)

class LoginSection(models.Model):
    User=models.ForeignKey(SignupSection,on_delete=models.CASCADE,default=None)
    MobileNumber=models.CharField(max_length=10)
    Password=models.CharField(max_length=50)
    LoginDateTime=models.DateTimeField(auto_now=True)
    LoginStatus=models.BooleanField(default=True)

class OrderDetails(models.Model):
    UserId=models.CharField(max_length=1000)
    ItemName=models.CharField(max_length=500)
    Cost=models.CharField(max_length=8)
    OrderDateTime=models.DateTimeField(auto_now=True)
