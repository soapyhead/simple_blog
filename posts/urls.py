from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostModelViewSet

router = DefaultRouter()
router.register(r'', PostModelViewSet)

urlpatterns = [
    path('', include(router.urls), name='posts'),
]