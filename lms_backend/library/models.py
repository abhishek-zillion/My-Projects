from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    modified_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    class Meta:
        abstract =True

class HomeCityChoices(models.Choices):
    SURAT='surat'
    BHARUCH='bharuch'
    BENGALURU='bengaluru'
    MUMBAI='mumbai'
    DELHI='delhi'
    KOLKATA='kolkata'
    HYDERABAD='hyderabad'
    CHANDIGARH='chandigarh'
    
class User(AbstractUser):
    STUDENT = 'STUDENT'
    LIBRARIAN = 'LIBRARIAN'
    USER_TYPE_CHOICES = ((STUDENT, 'Student'), (LIBRARIAN, 'Librarian'))

    user_type = models.CharField(
        choices=USER_TYPE_CHOICES, max_length=50, default=STUDENT)
    email = models.EmailField(unique=True, max_length=254)
    login_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    AVAILABLE = 'available'
    NOT_AVAILABLE = 'Not available'

    BOOK_STATUS = ((AVAILABLE, 'Available'), (NOT_AVAILABLE, 'Not Available'))
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=BOOK_STATUS, max_length=50)

    def __str__(self):
        return self.title


class BookRequest(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    RETURNED = 'RETURNED'
    REVOKED='REVOKED'

    REQUEST_STATUS = (
        (PENDING, 'Pending'), (APPROVED,
         'Approved'), (REJECTED, 'Rejected'), 
        (RETURNED,'Returned'),(REVOKED,'Revoked'))
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=REQUEST_STATUS,max_length=50,default=PENDING)
    approval_date=models.DateTimeField(null=True, blank=True)
    due_date=models.DateTimeField(null=True, blank=True)
    returned_date=models.DateTimeField(null=True, blank=True)    
    
    class Meta:
        indexes = [
            models.Index(fields=['user','status'],name='user_status_idx')
        ]
    
    def approve_request(self):
        if  self.status==self.PENDING:
            self.status = self.APPROVED
            self.approval_date=timezone.now()
            self.due_date=self.approval_date + timedelta(days=30)
            self.save()
            
            if self.book:
                self.book.stock-=1
                self.book.save()
    
    def rejected_request(self):
        if self.status==self.PENDING:
            self.status=self.REJECTED
            self.save()
    
    def revoked_request(self):
        if self.status == self.APPROVED:
            if self.book:
                self.book.stock+=1
                self.book.save()
            self.status=self.REVOKED
            self.save()
    
    def returned_request(self):
        if self.status== self.APPROVED:
            self.status=self.RETURNED
            self.returned_date=timezone.now()
            if self.book:
                self.book.stock+=1
                self.book.save()
            self.save()
    
    def __str__(self) -> str:
        return self.book.title

class UserProfile(TimeStampModel):
    user = models.OneToOneField(User,verbose_name='user_detail',related_name='user_profile',on_delete=models.PROTECT)
    home_city = models.CharField(choices=HomeCityChoices.choices,max_length=50,blank=True,null=True)
    
    def __str__(self) -> str:
        return self.user.username
    
class Tag(models.Model):
    id=models.AutoField(primary_key=True)
    tag_type = models.CharField(max_length=50,blank=True,null=True)
    book = models.ManyToManyField(Book,related_name='tags',related_query_name='tag')
    
    def __str__(self) -> str:
        return self.tag_type