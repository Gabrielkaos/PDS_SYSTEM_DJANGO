from django.core.exceptions import ValidationError
from django.utils import timezone
import re

def validate_philippine_mobile(value):
    """Validate Philippine mobile number format"""
    if not value:
        return
    
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', value)
    
    # Philippine mobile: +63 or 0 followed by 9XX-XXX-XXXX
    ph_pattern = r'^(\+63|0)?9\d{9}$'
    
    if not re.match(ph_pattern, cleaned):
        raise ValidationError(
            'Enter a valid Philippine mobile number (e.g., 09171234567 or +639171234567)'
        )

def validate_past_date(value):
    """Ensure date is not in the future"""
    if value and value > timezone.now().date():
        raise ValidationError('Date cannot be in the future')

def validate_birth_date(value):
    """Validate birth date (must be past, reasonable age)"""
    if not value:
        return
    
    today = timezone.now().date()
    
    if value > today:
        raise ValidationError('Birth date cannot be in the future')
    
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 15:
        raise ValidationError('Must be at least 15 years old')
    
    if age > 120:
        raise ValidationError('Invalid birth date (age cannot exceed 120 years)')

def validate_date_range(from_date, to_date):
    """Validate that to_date is after from_date"""
    if from_date and to_date and from_date > to_date:
        raise ValidationError('End date must be after start date')

def validate_philippine_zip(value):
    """Validate Philippine ZIP code (4 digits)"""
    if not value:
        return
    
    if not re.match(r'^\d{4}$', str(value)):
        raise ValidationError('Philippine ZIP code must be exactly 4 digits')

def validate_tin(value):
    """Validate Philippine TIN format"""
    if not value:
        return
    
    # TIN: XXX-XXX-XXX-XXX (12 digits, may have dashes)
    cleaned = re.sub(r'[\s\-]', '', value)
    
    if not re.match(r'^\d{9,12}$', cleaned):
        raise ValidationError('Invalid TIN format (9-12 digits)')

def validate_sss(value):
    """Validate Philippine SSS number"""
    if not value:
        return
    
    # SSS: XX-XXXXXXX-X (10 digits)
    cleaned = re.sub(r'[\s\-]', '', value)
    
    if not re.match(r'^\d{10}$', cleaned):
        raise ValidationError('Invalid SSS number (must be 10 digits)')

def validate_philhealth(value):
    """Validate PhilHealth number"""
    if not value:
        return
    
    # PhilHealth: XX-XXXXXXXXX-X (12 digits)
    cleaned = re.sub(r'[\s\-]', '', value)
    
    if not re.match(r'^\d{12}$', cleaned):
        raise ValidationError('Invalid PhilHealth number (must be 12 digits)')

def validate_rating(value):
    """Validate rating (0-100)"""
    if value is not None and (value < 0 or value > 100):
        raise ValidationError('Rating must be between 0 and 100')

def validate_year(value):
    """Validate year (4 digits, reasonable range)"""
    if not value:
        return
    
    try:
        year = int(value)
        current_year = timezone.now().year
        
        if year < 1900 or year > current_year + 10:
            raise ValidationError(f'Year must be between 1900 and {current_year + 10}')
    except (ValueError, TypeError):
        raise ValidationError('Invalid year format')