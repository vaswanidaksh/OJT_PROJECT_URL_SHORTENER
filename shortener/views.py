from django.shortcuts import render, redirect, get_object_or_404 #For redirecting, get 404 
from django.http import HttpResponseNotFound
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout  #For login and logout 
from .models import ShortURL
from .utils import generate_short_code
from rest_framework.generics import ListCreateAPIView 
from .serializers import ShortURLSerializer 
from rest_framework.permissions import AllowAny 
from .forms import ShortenerForm
import qrcode #Qr code library(for qrcode generation)
from io import BytesIO
import base64 #For our slug


# Create your views here.

@login_required
def home_view(request):
    new_url = None
    qr_code_base64 = None
    
    if request.method == 'POST':
        form = ShortenerForm(request.POST)
        if form.is_valid():
            short_url_obj = form.save()
            
            # Construct full short URL (e.g., http://localhost:8000/ABCD12)
            new_url = request.build_absolute_uri('/') + short_url_obj.short_code
            
            # QR CODE GENERATION (Stretch Goal)
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(new_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            
            # Convert image to base64 string to embed in HTML without saving to disk
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
    else:
        form = ShortenerForm()

    context = {
        'form': form,
        'new_url': new_url,
        'qr_code': qr_code_base64
    }
    return render(request, 'shortener/index.html', context)

# Redirecting url
def redirect_url_view(request, short_code):
    """Handles the redirection logic"""
    link = get_object_or_404(ShortURL, short_code=short_code)
    
    # Check Expiry
    if link.is_expired:
        return HttpResponseNotFound("<h1>This link has expired.</h1>")
        
    return redirect(link.original_url)

#For signup view
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log user in immediately after successful signup
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'shortener/signup.html', {'form': form})

#For login view
def custom_login_view(request):
    if request.user.is_authenticated: # Don't show login if already logged in
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

#For logout
def custom_logout_view(request):
    logout(request)
    # The redirect is handled by LOGOUT_REDIRECT_URL in settings.py,
    # but explicitly redirecting here works fine too.
    return redirect('home')


def index(request):
    # Your existing index view logic
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if not original_url:
            return render(request, 'shortener/index.html', {'error': 'URL cannot be empty.'})

        short_code = generate_short_code()
        short_url = ShortURL.objects.create(original_url=original_url, short_code=short_code)
        
        context = {
            'original_url': original_url,
            'short_url': request.build_absolute_uri('/') + short_code,
        }
        return render(request, 'shortener/index.html', context)

    return render(request, 'shortener/index.html')


def redirect_url(request, short_code):
    # Your existing redirect_url logic
    link = get_object_or_404(ShortURL, short_code=short_code)
    # Optional: You might want to increment a counter here
    return redirect(link.original_url)


# API View (NEW)

class ShortenerAPIView(ListCreateAPIView):
    
    # API endpoint that allows listing all short URLs (GET) and creating a new short URL (POST).
    # This view combines the logic for both methods.
    
    # Define the queryset (what data to list for GET)
    queryset = ShortURL.objects.all().order_by('-created_at')
    
    # Define the serializer (how to validate and format data)
    serializer_class = ShortURLSerializer
    
    # Define the permission (who can access this API)
    # AllowAny means anyone can access it (for public shortener)
    permission_classes = [AllowAny]
    
    # Override perform_create to inject the short code generation logic
    def perform_create(self, serializer):
        # Generate the short code before saving the validated data
        short_code = generate_short_code()
        serializer.save(short_code=short_code)
