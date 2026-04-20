from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import ShortURL
from .utils import generate_short_code
from rest_framework.generics import ListCreateAPIView
from .serializers import ShortURLSerializer
from rest_framework.permissions import AllowAny
from .forms import ShortenerForm
import qrcode
from io import BytesIO
import base64


# Create your views here.

def _generate_qr_base64(url):
    """Helper to generate a QR code as a base64-encoded PNG string."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


@login_required
def home_view(request):
    """
    Main shortener page.
    
    CORE FEATURE: If the submitted URL has already been shortened,
    we do NOT create a new entry — we return the existing short URL instead.
    """
    new_url = None
    qr_code_base64 = None
    already_existed = False

    if request.method == 'POST':
        form = ShortenerForm(request.POST)
        original_url = request.POST.get('original_url', '').strip()

        # ── Duplicate URL check ──────────────────────────────────
        # Look up by original_url BEFORE creating anything new.
        existing = ShortURL.objects.filter(original_url=original_url).first()

        if existing:
            # URL was already shortened — reuse the old record
            short_url_obj = existing
            already_existed = True
        elif form.is_valid():
            # New URL — save it (model.save auto-generates short_code)
            short_url_obj = form.save()
        else:
            # Form validation failed (invalid URL, etc.)
            context = {'form': form}
            return render(request, 'shortener/index.html', context)

        # Construct full short URL (e.g., http://localhost:8000/ABCD12)
        new_url = request.build_absolute_uri('/') + short_url_obj.short_code

        # QR CODE GENERATION
        qr_code_base64 = _generate_qr_base64(new_url)

        # Reset the form so the input field is empty after submission
        form = ShortenerForm()

    else:
        form = ShortenerForm()

    context = {
        'form': form,
        'new_url': new_url,
        'qr_code': qr_code_base64,
        'already_existed': already_existed,
    }
    return render(request, 'shortener/index.html', context)


# Redirecting url
def redirect_url_view(request, short_code):
    """Handles the redirection logic with expiry checking."""
    link = get_object_or_404(ShortURL, short_code=short_code)

    # Check Expiry
    if link.is_expired:
        return render(request, 'shortener/error.html', {
            'message': 'This link has expired and is no longer available.'
        })

    return redirect(link.original_url)


# For signup view
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log user in immediately after successful signup
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'shortener/signup.html', {'form': form})


# For login view
def custom_login_view(request):
    if request.user.is_authenticated:  # Don't show login if already logged in
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'shortener/login.html', {'form': form})


# For logout
def custom_logout_view(request):
    logout(request)
    return redirect('home')


# ── API View ─────────────────────────────────────────────────────
class ShortenerAPIView(ListCreateAPIView):
    """
    API endpoint that allows listing all short URLs (GET)
    and creating a new short URL (POST).

    DUPLICATE PREVENTION: If the original_url already exists,
    the existing record is returned instead of creating a duplicate.
    """
    queryset = ShortURL.objects.all().order_by('-created_at')
    serializer_class = ShortURLSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        original_url = serializer.validated_data.get('original_url')

        # Check if this URL was already shortened
        existing = ShortURL.objects.filter(original_url=original_url).first()
        if existing:
            # Instead of creating a new one, we'll return the existing object.
            # We override the serializer's instance so the response uses it.
            serializer.instance = existing
            return

        # New URL — generate a short code and save
        short_code = generate_short_code()
        serializer.save(short_code=short_code)
