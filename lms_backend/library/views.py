from celery.result import AsyncResult
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.signals import user_logged_in
from rest_framework.response import Response
from library.models import Book, BookRequest, User
from library.permissions import IsLibrarian
from library.serializers import *
from rest_framework.views import APIView
from rest_framework import permissions, status, authentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from rest_framework import generics
from django.utils import timezone
from library.tasks import process_book_return,notify_librarian,book_request_count
from .signals import *

# Signup View
class UserSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                student=request.user
                student.last_login=timezone.now()
                student.save()
                token, created = Token.objects.get_or_create(user=user)
                data=serializer.data 
                data['token']='token '+ token.key
                data['user_type']=user.user_type
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'unable to login with provided credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        user = request.user
        print(user)
        if user.is_authenticated:
            Token.objects.get(user=user).delete()
            logout(request)
            return Response({'message': "Logout successful"}, status=status.HTTP_200_OK)
        return Response({'message': "User is not authenticated"})

# listing all book

class AllBooksView(generics.ListAPIView):
    queryset = Book.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        user = self.request.user
        if user.user_type == User.STUDENT:
            return BookSerializer
        return LibrarianBookSerializer
    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        queryset = super().get_queryset()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query))

        return queryset.order_by('id')


# librarian can add book , same denies to student


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.user_type == 'LIBRARIAN':
            serializer.save()
        else:
            raise PermissionDenied(
                detail="You don't have permission to perform this action.")

# librarian can update book ,same denies to student


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.user_type == User.LIBRARIAN:
            serializer.save()
        else:
            raise PermissionDenied(
                detail="Student don't have permission to update book.")

    def perform_destroy(self, instance):
        if self.request.user.user_type == User.LIBRARIAN:
            instance.delete()
        else:
            raise PermissionDenied(
                detail="Student don't have permission to delete this book.")

# student can request book
class BookRequestView(generics.CreateAPIView):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.user_type == 'STUDENT':  # Check if the user is a student
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            student=request.user.username
            book_id=serializer.validated_data.get('book_id')
            book_request_count.delay(int(book_id))
            notify_librarian.delay(student)       

            return Response({'msg': 'Book request created successfully',}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Only students can request books'}, status=status.HTTP_403_FORBIDDEN)

# librarian action on bookrequest
class BookRequestActionView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookRequestActionSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            book_request_id = self.kwargs.get('pk')
            book_request = get_object_or_404(BookRequest, id=book_request_id)

            if request.user.user_type == User.LIBRARIAN:
                if book_request.book.stock == 0:
                    return Response({'message': "Book is currently unavailable"}, status=status.HTTP_400_BAD_REQUEST)
                if action == BookRequest.APPROVED:
                    book_request.approve_request()
                elif action == BookRequest.REJECTED:
                    book_request.rejected_request()
                elif action == BookRequest.REVOKED:
                    book_request.revoked_request()
                else:
                    return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': f'Action: {action} performed successfully on {book_request.book.title}'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Only librarians can perform this action'},
                                status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# book viewed by user and student


class AllBookRequestsView(generics.ListAPIView):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'LIBRARIAN':
            return BookRequest.objects.all()
        else:
            return BookRequest.objects.filter(user=user)

# student returning book


class ReturnBookView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReturnBookSerializer(data=request.data)
        if serializer.is_valid():
            request_id = serializer.validated_data['request_id']
            try:
                book_request = BookRequest.objects.get(
                    id=request_id, user=request.user)
                if book_request.status == BookRequest.APPROVED:
                    process_book_return.apply_async(args=[request_id])
                    return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Book request is not approved'}, status=status.HTTP_400_BAD_REQUEST)
            except BookRequest.DoesNotExist:
                return Response({'error': 'Book request not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Book request history
class BookRequestHistory(generics.ListAPIView):
    authentication_classe = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompleteBookRequestSerializer

    def get_queryset(self,):
        user = self.request.user
        if user.user_type == User.LIBRARIAN:
            return BookRequest.objects.all()
        else:
            return BookRequest.objects.filter(user=user)

class RegisteredStudentView(generics.ListAPIView):
    authentication_classe = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisteredStudentSerializer


    def get_queryset(self):
        user = self.request.user
        if user.user_type == User.LIBRARIAN:
            return User.objects.filter(user_type=User.STUDENT)    
        else:
            return User.objects.filter(user=self.request.user)