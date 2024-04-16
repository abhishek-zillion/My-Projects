from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator,MaxLengthValidator,MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

def alphanumeric(value):
    if not str(value).isalnum():
        raise ValidationError('Only alphanumeric characters are allowed.')
    return value


class Showroomlist(models.Model):
    name = models.CharField(("Name "), max_length=150)
    location = models.CharField(("Location"), max_length=150)
    website = models.URLField(("URL"), max_length=200)
    
    def __str__(self):
        return self.name


class Carlist(models.Model):
    name = models.CharField("Name", max_length=150)
    description = models.CharField(("Desc"), max_length=150)
    active = models.BooleanField(default=False)
    chassis_number = models.CharField(("Chasis Number"), max_length=50, blank=True, null=True,
                                      validators=[alphanumeric])
    price = models.DecimalField(
        "Price", max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey(Showroomlist,on_delete=models.CASCADE,related_name='showrooms',null=True)
    def __str__(self):
        return self.name

    
class Review(models.Model):
    apiuser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    rating=models.IntegerField(("Rating"),validators=[MinValueValidator(0),MaxValueValidator(10)],null=True,blank=True)
    comments=models.CharField(("Comment"),max_length=400,null=True,blank=True)
    car=models.ForeignKey(Carlist,related_name='reviews', on_delete=models.CASCADE,null=True,blank=True)
    updated_at=models.DateTimeField(("Created At"), auto_now=True,)
    created_at=models.DateTimeField(("Created At"), auto_now_add=True,)
    
    def __str__(self):   
        return f' rating of {str(self.rating)}'
