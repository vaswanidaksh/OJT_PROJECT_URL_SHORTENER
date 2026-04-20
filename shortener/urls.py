from django.urls import path
from . import views
from .views import ShortenerAPIView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),

    # API endpoint
    path('api/links/', ShortenerAPIView.as_view(), name='api_links'),

    # Short code redirect — MUST be last so it doesn't swallow other routes
    path('<str:short_code>', views.redirect_url_view, name='redirect'),
]