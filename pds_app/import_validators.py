from django.core.exceptions import ValidationError
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import re

class ImportDataValidator:
    
    
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.errors = []
        self.warnings = []
    
    def add_error(self, field, message):
        self.errors.append(f"{field}: {message}")
    
    def add_warning(self, field, message):
        self.warnings.append(f"{field}: {message}")
    
    def has_errors(self):
        return len(self.errors) > 0
    
    def get_error_summary(self):
        if not self.has_errors():
            return None
        return f"Sheet '{self.sheet_name}' - Validation Errors:\n" + "\n".join(f"  • {err}" for err in self.errors)
    
    def validate_required_field(self, value, field_name):
        if not value or str(value).strip() == "":
            self.add_error(field_name, "This field is required")
            return False
        return True
    
    def validate_birth_date(self, value):
        if not value:
            self.add_error("Date of Birth", "Required field")
            return None
        
        try:
            if isinstance(value, date):
                birth_date = value
            else:
                birth_date = datetime.strptime(str(value), "%Y-%m-%d").date()
            
            today = date.today()
            
            if birth_date > today:
                self.add_error("Date of Birth", "Cannot be in the future")
                return None
            
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            if age < 15:
                self.add_error("Date of Birth", "Person must be at least 15 years old")
                return None
            
            if age > 120:
                self.add_error("Date of Birth", "Invalid birth date (age exceeds 120 years)")
                return None
            
            return birth_date
            
        except Exception as e:
            self.add_error("Date of Birth", f"Invalid date format: {e}")
            return None
    
    def validate_mobile_number(self, value):
        if not value:
            return value
        
        cleaned = re.sub(r'[\s\-\(\)]', '', str(value))
        
        if not re.match(r'^(\+63|0)?9\d{9}$', cleaned):
            self.add_warning("Mobile Number", "Invalid Philippine mobile format (expected: 09171234567)")
        
        return value
    
    def validate_email(self, value):
        if not value:
            return value
        
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, str(value)):
            self.add_warning("Email", "Invalid email format")
        
        return value
    
    def validate_zip_code(self, value, field_name="ZIP Code"):
        if not value:
            return value
        
        if not re.match(r'^\d{4}$', str(value)):
            self.add_warning(field_name, "Philippine ZIP code should be 4 digits")
        
        return value
    
    def validate_height(self, value):
        if not value:
            return 0
        
        try:
            height = float(value)
            if height < 50 or height > 300:
                self.add_error("Height", "Must be between 50 and 300 cm")
                return 0
            return Decimal(str(height))
        except (ValueError, InvalidOperation):
            self.add_error("Height", "Invalid number format")
            return 0
    
    def validate_weight(self, value):
        if not value:
            return 0
        
        try:
            weight = float(value)
            if weight < 20 or weight > 300:
                self.add_error("Weight", "Must be between 20 and 300 kg")
                return 0
            return Decimal(str(weight))
        except (ValueError, InvalidOperation):
            self.add_error("Weight", "Invalid number format")
            return 0
    
    def validate_sex(self, value):
        if not value:
            self.add_error("Sex", "Required field")
            return ""
        
        value = str(value).strip().capitalize()
        if value not in ['Male', 'Female']:
            self.add_error("Sex", "Must be 'Male' or 'Female'")
            return ""
        
        return value
    
    def validate_civil_status(self, value):
        if not value:
            self.add_error("Civil Status", "Required field")
            return ""
        
        valid_statuses = ['Single', 'Married', 'Widowed', 'Divorced', 'Separated']
        value = str(value).strip().capitalize()
        
        if value not in valid_statuses:
            self.add_error("Civil Status", f"Must be one of: {', '.join(valid_statuses)}")
            return ""
        
        return value
    
    def validate_blood_type(self, value):
        if not value:
            return ""
        
        valid_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        value = str(value).strip().upper()
        
        if value not in valid_types:
            self.add_warning("Blood Type", f"Should be one of: {', '.join(valid_types)}")
        
        return value
    
    def validate_tin(self, value):
        if not value:
            return value
        
        cleaned = re.sub(r'[\s\-]', '', str(value))
        if not re.match(r'^\d{9,12}$', cleaned):
            self.add_warning("TIN", "Should be 9-12 digits")
        
        return value
    
    def validate_sss(self, value):
        if not value:
            return value
        
        cleaned = re.sub(r'[\s\-]', '', str(value))
        if not re.match(r'^\d{10}$', cleaned):
            self.add_warning("SSS", "Should be 10 digits")
        
        return value
    
    def validate_philhealth(self, value):
        if not value:
            return value
        
        cleaned = re.sub(r'[\s\-]', '', str(value))
        if not re.match(r'^\d{12}$', cleaned):
            self.add_warning("PhilHealth", "Should be 12 digits")
        
        return value
    
    def validate_date_range(self, from_date, to_date, context=""):
        if not from_date or not to_date:
            return True
        
        try:
            if isinstance(from_date, str):
                from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
            else:
                from_dt = from_date
            
            if isinstance(to_date, str):
                to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
            else:
                to_dt = to_date
            
            if from_dt > to_dt:
                self.add_error(f"{context} Date Range", "End date must be after start date")
                return False
            
            return True
            
        except Exception as e:
            self.add_error(f"{context} Date Range", f"Invalid date format: {e}")
            return False
    
    def validate_past_date(self, value, field_name):
        if not value:
            return value
        
        try:
            if isinstance(value, str):
                date_val = datetime.strptime(value, "%Y-%m-%d").date()
            else:
                date_val = value
            
            if date_val > date.today():
                self.add_warning(field_name, "Date is in the future")
            
            return date_val
            
        except Exception as e:
            self.add_error(field_name, f"Invalid date: {e}")
            return None
    
    def validate_rating(self, value):
        if not value:
            return None
        
        try:
            rating = float(value)
            if rating < 0 or rating > 100:
                self.add_error("Rating", "Must be between 0 and 100")
                return None
            return Decimal(str(rating))
        except (ValueError, InvalidOperation):
            self.add_error("Rating", "Invalid number format")
            return None
    
    def validate_positive_integer(self, value, field_name):
        if not value:
            return 0
        
        try:
            num = int(value)
            if num < 0:
                self.add_warning(field_name, "Should be a positive number")
                return 0
            return num
        except (ValueError, TypeError):
            self.add_error(field_name, "Invalid number format")
            return 0
    
    def validate_decimal(self, value, field_name):
        if not value:
            return None
        
        try:
            return Decimal(str(value))
        except InvalidOperation:
            self.add_error(field_name, "Invalid decimal format")
            return None
    
    def validate_year(self, value, field_name):
        if not value:
            return ""
        
        try:
            year = int(value)
            current_year = date.today().year
            
            if year < 1900 or year > current_year + 10:
                self.add_warning(field_name, f"Year should be between 1900 and {current_year + 10}")
        except (ValueError, TypeError):
            self.add_warning(field_name, "Invalid year format")
        
        return str(value)