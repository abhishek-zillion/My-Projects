from datetime import timedelta
from celery import shared_task
from time import sleep
from library.models import BookRequest, Book,User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task(name='reject_book_request')
def reject_book_request():
    pending_requests = BookRequest.objects.all()

    for req_obj in pending_requests:
        if req_obj.status == BookRequest.PENDING:
            if req_obj.user.username == 'student1':
                req_obj.status = BookRequest.REJECTED
                req_obj.save()
                print('request rejected of student1')
    return 'No new requests'

@shared_task(name='stock_check')
def stock_check(*args, **kwargs):
    message = args[0]
    recipient = kwargs.get('recipient','apagrawal26@gmail.com')
    book_queryset = Book.objects.all()
    for book in book_queryset:
        if book.stock == 0:
            send_mail(
                subject=f'{message}:Book is out of stock',
                message=f'Immediately fill this  "{book.title} book"',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
            )
            return f"{book.title},is currently unavailable"
    return 'All books are in stock'
    


@shared_task(name='notify_librarian')
def notify_librarian(student):
    sleep(5)
    librarian_email = 'abhishekwagh420@gmail.com'
    send_mail(
        subject='New Book Request',
        message=f'{student} has requested a book',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[librarian_email],
    )
    return f'email is sent regarding {student} student'
    
@shared_task(name='process_book_return')
def process_book_return(request_id):
    try:
        sleep(30)
        print(request_id)
        book_request = BookRequest.objects.get(id=request_id)
        if book_request.status == BookRequest.APPROVED:
            book_request.returned_request()
            return {'success': True, 'message': 'Book returned successfully'}
        else:
            return {'success': False, 'message': 'Book request is not approved'}
    except BookRequest.DoesNotExist:
        return {'success': False, 'message': 'Book request not found'}

@shared_task(name='book_request_count')
def book_request_count(book_id):
    try:
        book_requests = BookRequest.objects.filter(book_id=book_id)
        book_request_count = len(book_requests)
        
        if book_request_count >= 5:
            librarian_email = 'abhishekwagh420@gmail.com'
            subject = f'Book Requests Exceeded for Book ID {book_id}'
            message = f'The number of requests for book with ID {book_id} has exceeded the threshold (5 requests). Please take action.'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[librarian_email],
            )
            return {'success': True, 'message': f'Alert sent to the librarian for book ID {book_id}'}
        else:
            return {'success': False, 'message': f'No alert sent to the librarian for book ID {book_id}'}
    except Exception as e:
        return {'success': False, 'message': f'Error occurred: {str(e)}'}


@shared_task(name='show_recent_logins')
def show_recent_logins():
    threshold_time = timezone.now() - timedelta(seconds=60)
    recent_logins = User.objects.filter(login_time__gte=threshold_time)
    recent_logins_count = len(recent_logins)
    users=''
    for user in recent_logins:
        print(f"User {user.username} logged in recently at {user.login_time}")
        users+=f"{user.username},"
    return {'success': True, 'users':users, 'count':recent_logins_count}