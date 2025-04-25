from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload/', views.image_upload, name='image_upload'),
    path('category/<str:category_id>/', views.category_detail, name='category_detail'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('logout/', views.custom_logout, name='logout'),
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
]
