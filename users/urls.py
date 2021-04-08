from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include([
        path('email/', views.get_confirmation_code),
        path('token/', views.get_jwt_token),
    ])),

]
