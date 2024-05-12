
from django.contrib import admin
from django.urls import path,include
from library import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),  # Browsable API login/logout
    # path('api/token/', obtain_auth_token),  # Token authentication
    path('admin/', admin.site.urls),
    
    path('signup/',views.UserSignUpView.as_view()),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='custom-logout'),
    path('allbooks/',views.AllBooksView.as_view(),name='allbooks'), #all books and retrieving
    path('listbook/', views.BookListView.as_view(), name='list-book'), #add book
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'), #update,delete book
    path('books/request/',views.BookRequestView.as_view(),name='book-request'), #by student
    path('books/<int:pk>/action/',views.BookRequestActionView.as_view(),name='book-request-action'),#on bookrequest
    # path('book-requests/', views.AllBookRequestsView.as_view(), name='all-book-requests'),#all book reqs
    path('return-book/', views.ReturnBookView.as_view(), name='return-book'),#by student
    path('bookreq-history/',views.BookRequestHistory.as_view(),name='book_requests'),#all book reqs
    path('registered-students/',views.RegisteredStudentView.as_view(),name='registered-students'),# all registered students
]
