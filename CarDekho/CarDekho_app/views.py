from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework import generics, mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from CarDekho_app.permissions import AdminOrReadonlyPermission, ReviewUserOrReadOnly
from CarDekho_app.models import Carlist, Showroomlist, Review
from CarDekho_app.serializers import CarSerializer, ShowroomSerializer, ReviewSerializer
from CarDekho_app.throttling import ReviewFullDetailThrottle, ReviewDetailThrottle
from CarDekho_app.pagination import ReviweFullDetailPagination,ReviewFullDetailLimitOffsetPag


class CarListView(APIView):
    def get(self, request):
        cars = Carlist.objects.all()
        serializer = CarSerializer(
            cars, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CarDetailView(APIView):

    def get(self, request, pk):
        try:
            car = Carlist.objects.get(pk=pk,)
            serializer = CarSerializer(car,)
            return Response(serializer.data)
        except Carlist.DoesNotExist:
            return Response("Car not found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        Carlist.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowroomView(viewsets.ViewSet):

    def list(self, request):
        showroom = Showroomlist.objects.all()
        serializer = ShowroomSerializer(
            showroom, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None,):
        showroom = Showroomlist.objects.all()
        obj = get_object_or_404(showroom, pk=pk)
        serializer = ShowroomSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        obj = Showroomlist.objects.create(data=request.data)
        serializer = ShowroomSerializer(obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        obj = Showroomlist.objects.get(pk=pk)
        serializer = ShowroomSerializer(obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewCreateView(generics.CreateAPIView,):
    serializer_class = ReviewSerializer
    # permission_classes=[AdminOrReadonlyPermission]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        cars = Carlist.objects.get(pk=pk)
        current_user = self.request.user
        review_queryset = Review.objects.filter(
            car=cars, apiuser=current_user,)
        if review_queryset.exists():
            print(review_queryset)
            raise serializers.ValidationError(
                "You have already reviewed this car")
        return serializer.save(car=cars, apiuser=current_user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(data={"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class ReviewView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self,):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except:
            return Response("Review not found", status=status.HTTP_404_NOT_FOUND)


class ReviewDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    # throttle_classes = [ReviewDetailThrottle]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewFullDetailView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    # pagination_class = ReviweFullDetailPagination
    # throttle_classes=[ReviewFullDetailThrottle]
    pagination_class=ReviewFullDetailLimitOffsetPag
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
