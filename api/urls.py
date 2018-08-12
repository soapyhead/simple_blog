from django.urls import path, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Blog API')


urlpatterns = [
    path('', include('accounts.urls')),
    path('posts/', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('auth/', include('rest_framework.urls')),
        path('docs/', schema_view)
    ]
