from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Django's built-in User model
# from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import signuppage 
from django.contrib.auth import authenticate, login

# Create your views here.
def legallens(req):
    return render(req, 'app1/core.html')


def main(req):
    return render(req, 'app1/main.html')

def signup(req):
    return render(req, 'app1/sign.html')

def loginpage(req):
    return render(req,'app1/LoginPage.html')


def userdetail(req):
    return render(req, 'app1/userdetail.html')

def SignUpPage(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # user_entry = signuppage(first_name=first_name, last_name=last_name,email=email,password=password, date=datetime.today())
        # user_entry.save()
        print("Received POST request")
        
         # ✅ Check if user already exists in the auth system
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!", extra_tags="danger")
            print("Error message added!")
            return render(request, 'app1/loginpage.html')
        user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
                
         
        messages.success(request, "Account created successfully!", extra_tags="success")
        print("Success message added!")
        return redirect('loginpage')  
    return render(request, 'app1/SignUpPage.html')  # Show signup page for GET request

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def loginpage(request):
    # For debugging - always log when this view is accessed
    print("Login view accessed")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        print(f"Login attempt with email: {email}")
        
        # First check if a user with this email exists
        try:
            user = User.objects.get(email=email)
            print(f"User found with email {email}, username: {user.username}")
            
            # Try to authenticate
            user_auth = authenticate(request, username=user.username, password=password)
            
            if user_auth is not None:
                # Authentication successful
                print(f"Authentication successful for {email}")
                login(request, user_auth)
                messages.success(request, "Login successful!" , extra_tags="Success")
                print("Redirecting to main page")
                return redirect("main")  # Make sure 'main' matches your URL name
            else:
                # Password didn't match
                print(f"Authentication failed - incorrect password for {email}")
                messages.error(request, "Invalid password." , extra_tags="danger")
                return render(request, "app1/LoginPage.html")
                
        except User.DoesNotExist:
            # No user with this email
            print(f"No user found with email: {email}")
            messages.error(request, "Email not registered.",extra_tags="Success")
            return render(request, "app1/LoginPage.html")
    
    # GET request or any other method
    return render(request, "app1/LoginPage.html")

def result(request):
    return render(request, "app1/result.html")






import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import PyPDF2
import docx
import io
from django.conf import settings

# Configure Gemini API
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

def home(request):
    return render(request, 'app1/core.html')

def signuppage(request):
    # Your signup logic here
    return render(request, 'app1/signup.html')

# def extract_text_from_pdf(file_bytes):
#     """Extract text from PDF file bytes"""
#     pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# def extract_text_from_docx(file_bytes):
#     """Extract text from DOCX file bytes"""
#     doc = docx.Document(io.BytesIO(file_bytes))
#     text = ""
#     for para in doc.paragraphs:
#         text += para.text + "\n"
#     return text

# @csrf_exempt
# def analyse_document(request):
#     """Process uploaded document and analyze with Gemini API"""
#     if request.method != 'POST':
#         return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})

#     if 'document' not in request.FILES:
#         return JsonResponse({'success': False, 'error': 'No document provided'})

#     uploaded_file = request.FILES['document']
#     file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
#     try:
#         # Read file content
#         file_bytes = uploaded_file.read()
        
#         # Extract text based on file type
#         if file_extension == '.pdf':
#             extracted_text = extract_text_from_pdf(file_bytes)
#         elif file_extension in ['.doc', '.docx']:
#             extracted_text = extract_text_from_docx(file_bytes)
#         else:
#             return JsonResponse({'success': False, 'error': 'Unsupported file format'})
        
#         # Check if text was extracted successfully
#         if not extracted_text or len(extracted_text) < 10:
#             return JsonResponse({'success': False, 'error': 'Could not extract text from document'})
        
#         # Prepare prompt for Gemini
#         prompt = f"""Analyze the following legal document:

# {extracted_text[:15000]}  # Limiting to 15000 chars to avoid token limits

# Please provide:
# 1. Identify any risky clauses
# 2. Summarize the key points of the document
# 3. Provide overall risk assessment

# Format your response in HTML with appropriate classes for styling:
# - Use <div class="risky-clause"> for risky clauses
# - Use <div class="safe-clause"> for safe clauses
# - Use <div class="summary-section"> for the summary section
# """

#         # Call Gemini API
#         model = genai.GenerativeModel('gemini-1.5-pro')
#         response = model.generate_content(prompt)
        
#         # Format the response
#         analysis_results = response.text
        
#         return JsonResponse({
#             'success': True,
#             'results': analysis_results
#         })
        
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)})







import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from app1.gemini_api import analyze_text  # You’ll create this helper
from PyPDF2 import PdfReader

def upload_file(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        file_url = fs.url(filename)
        is_pdf = filename.lower().endswith('.pdf')


        # Extract text (example with PDF)
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        # Send to Gemini API
        analysis = analyze_text(text)

        # Pass result to result page
        # Just an example
        return render(request, 'app1/result.html', {
            'risky_clauses': analysis.get('risky_clauses', 'No risky clauses found.'),
            'summary': analysis.get('summary', 'No summary available.'),
            'clause_check': analysis.get('clause_check', 'No clause check data.'),
            'file_url': file_url,
            'file_name': filename,
            'is_pdf': is_pdf 
        })

    
    
    

    return redirect('upload_file')
