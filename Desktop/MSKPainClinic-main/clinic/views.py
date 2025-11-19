from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact, ContactSubmission
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache
import re
import logging

# Set up logger (without PII)
logger = logging.getLogger(__name__)

@cache_page(60 * 15)  # Cache for 15 minutes
@vary_on_cookie
def home(request):
    return render(request, 'home.html')

@cache_page(60 * 15)
@vary_on_cookie
def treatment(request):
    return render(request, 'treatment.html')

def contact(request):
    # Store success message in session if it exists
    stored_message = request.session.pop('success_message', None)
    if stored_message:
        messages.success(request, stored_message)
    context = {
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY
    }
    return render(request, 'contact.html', context)

@cache_page(60 * 15)
@vary_on_cookie
def contacts(request):
    """Contact information page (Контакты)"""
    return render(request, 'contacts.html')

def thank_you(request):
    """Thank you page after successful form submission"""
    return render(request, 'thank_you.html')

@require_POST
def submit_contact(request):
    # Rate limiting: 1 submission per hour per IP
    ip_address = request.META.get('REMOTE_ADDR', 'unknown')
    rate_limit_key = f'submit_contact_{ip_address}'
    submission_count = cache.get(rate_limit_key, 0)
    
    if submission_count >= 1:
        logger.warning(f"Rate limit exceeded for IP: {ip_address}")
        messages.error(request, 'Слишком много запросов. Пожалуйста, попробуйте позже.')
        return redirect('contact')
    
    try:
        # Get form data
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        pain_locations = request.POST.get('pain_locations', '').split(',')
        pain_duration = request.POST.get('pain_duration', '').strip()
        pain_level = request.POST.get('pain_level', '').strip()
        message = request.POST.get('message', '').strip()
        patient_type = request.POST.get('patient_type', 'self-paying').strip()
        consent = 'consent' in request.POST

        # Log form submission (without PII)
        logger.info(f"Contact form submission received from IP: {ip_address}")

        # Validate required fields
        required_fields = {
            'last_name': {
                'value': last_name,
                'error': 'Пожалуйста, введите фамилию'
            },
            'first_name': {
                'value': first_name,
                'error': 'Пожалуйста, введите имя'
            },
            'contact_email': {
                'value': contact_email,
                'error': 'Пожалуйста, введите email'
            },
            'mobile': {
                'value': mobile,
                'error': 'Пожалуйста, введите номер телефона'
            },
            'consent': {
                'value': consent,
                'error': 'Необходимо ваше согласие для отправки формы'
            }
        }

        # Check for missing required fields
        missing_fields = []
        for field_name, field_data in required_fields.items():
            if not field_data['value']:
                missing_fields.append(field_name)
                messages.error(request, field_data['error'])

        if missing_fields:
            logger.info(f"Form validation failed - missing fields: {missing_fields}")
            return redirect('contact')

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', contact_email):
            messages.error(request, 'Пожалуйста, введите корректный email адрес')
            return redirect('contact')

        # Validate phone number format
        phone_number = re.sub(r'\D', '', mobile)
        if not (len(phone_number) == 11 and phone_number.startswith('7') and phone_number[1] in '123456789'):
            messages.error(request, 'Пожалуйста, введите корректный номер телефона')
            return redirect('contact')

        # Create new contact submission
        submission = ContactSubmission.objects.create(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            contact_email=contact_email,
            mobile=mobile,
            pain_locations=pain_locations,
            pain_duration=pain_duration,
            pain_level=pain_level,
            message=message,
            patient_type=patient_type,
            consent=consent
        )

        # Increment rate limit counter (expires in 1 hour)
        cache.set(rate_limit_key, submission_count + 1, 3600)
        
        logger.info(f"Contact form submission successful - ID: {submission.id}")
        return redirect('thank_you')

    except Exception as e:
        # Log error without exposing sensitive data
        logger.error(f"Error in submit_contact: {type(e).__name__}", exc_info=True)
        messages.error(request, 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.')
        return redirect('contact')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms(request):
    return render(request, 'terms.html')

def assessment(request):
    return render(request, 'assessment.html')

def test(request):
    return render(request, 'test.html')

def test2(request):
    return render(request, 'test2.html')

@require_POST
def submit_assessment(request):
    # Rate limiting: 1 submission per hour per IP
    ip_address = request.META.get('REMOTE_ADDR', 'unknown')
    rate_limit_key = f'submit_assessment_{ip_address}'
    submission_count = cache.get(rate_limit_key, 0)
    
    if submission_count >= 1:
        logger.warning(f"Rate limit exceeded for assessment form - IP: {ip_address}")
        return JsonResponse({
            'status': 'error',
            'message': 'Слишком много запросов. Пожалуйста, попробуйте позже.'
        }, status=429)
    
    try:
        # Get form data
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        region = request.POST.get('region', '').strip()
        
        # Get pain assessment data
        pain_areas = request.POST.getlist('pain_areas')
        pain_duration = request.POST.get('pain_duration', '')
        pain_type = request.POST.getlist('pain_type')
        has_scans = request.POST.get('has_scans') == 'on'
        comments = request.POST.get('comments', '').strip()
        
        # Log submission (without PII)
        logger.info(f"Assessment form submission received from IP: {ip_address}")
        
        # Here you would typically save this data to your database
        # For now, we'll just return a success response
        
        # Increment rate limit counter (expires in 1 hour)
        cache.set(rate_limit_key, submission_count + 1, 3600)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Assessment submitted successfully'
        })
        
    except Exception as e:
        # Log error without exposing sensitive data
        logger.error(f"Error in submit_assessment: {type(e).__name__}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте еще раз.'
        }, status=400)
