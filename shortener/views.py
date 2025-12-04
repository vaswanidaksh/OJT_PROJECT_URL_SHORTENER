from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import timezone

from .models import ShortURL
from .forms import ShortenerForm
from .utils import generate_short_code

import qrcode
from io import BytesIO
import base64

# ---------------------------
# HOME (SHORTENER PAGE)
# ---------------------------
def home_view(request):
    short_url = None
    qr_code = None

    if request.method == "POST":
        form = ShortenerForm(request.POST)
        if form.is_valid():
            short_url_obj = form.save(commit=False)

            # Save user ONLY if logged in
            if request.user.is_authenticated:
                short_url_obj.user = request.user
            else:
                short_url_obj.user = None

            short_url_obj.save()

            short_url = request.build_absolute_uri('/') + short_url_obj.short_code

            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(short_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

    else:
        form = ShortenerForm()

    return render(request, "shortener/index.html", {
        "form": form,
        "short_url": short_url,
        "qr_code": qr_code
    })


# ---------------------------
# REDIRECTION PAGE
# ---------------------------
def redirect_url(request, short_code):
    link = get_object_or_404(ShortURL, short_code=short_code)

    if link.is_expired:
        return HttpResponseNotFound("<h1>This link has expired.</h1>")

    return redirect(link.original_url)


# ---------------------------
# SIGNUP
# ---------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Required when multiple auth backends exist
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "shortener/signup.html", {"form": form})


# ---------------------------
# LOGIN
# ---------------------------
def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "shortener/login.html", {"form": form})


# ---------------------------
# LOGOUT
# ---------------------------
def custom_logout_view(request):
    logout(request)
    return redirect("login")


# ---------------------------
# HISTORY PAGE (USER-SPECIFIC)
# ---------------------------
@login_required
def history(request):
    urls = ShortURL.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "shortener/history.html", {"urls": urls})


# ---------------------------
# STATIC PAGES
# ---------------------------
def features(request):
    return render(request, "shortener/features.html")


def about(request):
    return render(request, "shortener/about.html")


# ---------------------------
# API VIEW (DRF)
# ---------------------------
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import ShortURLSerializer

class ShortenerAPIView(ListCreateAPIView):
    """
    API endpoint that allows listing all short URLs (GET) and creating new short URLs (POST)
    """
    queryset = ShortURL.objects.all().order_by('-created_at')
    serializer_class = ShortURLSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(short_code=generate_short_code())
