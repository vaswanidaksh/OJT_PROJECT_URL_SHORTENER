from django.urls import path
from . import views
from .views import ShortenerAPIView

urlpatterns = [
    # Web pages
    path('', views.home_view, name='home'),  # Homepage
    path('features/', views.features, name='features'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Short URL redirect
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),

    # API endpoint
    path('api/links/', ShortenerAPIView.as_view(), name='api_links'),
]
