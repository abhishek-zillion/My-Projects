from django.urls import path, include
from rest_framework.routers import DefaultRouter
from CarDekho_app import views

router = DefaultRouter()
router.register('showroom', views.ShowroomView, basename='showroom')
# router.register('review', views.ReviewView, basename='review')

urlpatterns = [
    path('list/', views.CarListView.as_view(), name='car_list'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),

    path('', include(router.urls)),
    path('showroom/<int:pk>/review-create/',
         views.ReviewCreateView.as_view(), name='review_create'),
    path('showroom/<int:pk>/review/',
         views.ReviewView.as_view(), name='review_list'),
    path('showroom/review/<int:pk>/',
         views.ReviewDetailView.as_view(), name='review_detail'),
    path('comments/', views.ReviewFullDetailView.as_view(),
         name='review_detail_full'),



]
