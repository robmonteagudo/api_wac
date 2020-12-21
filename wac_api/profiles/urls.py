# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from profiles import views as user_views

router = DefaultRouter()
router.register(r'profiles', user_views.UserViewSet, basename='profiles')
router.register(r'profiles', user_views.EditViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('profiles/password', user_views.ChangePasswordView.as_view()),
]