from django import forms
from .models import PersonalInformation, EducationalBackground, FamilyBackground
from .models import OtherInformation

class ImportForm(forms.Form):
    file = forms.FileField(label="Choose Excel File")

class OtherInformationForm(forms.ModelForm):
    class Meta:
        model = OtherInformation
        fields = '__all__'  # Include all fields from the model
        exclude = ['date_accomplished', 'user']
        widgets = {
            'with_third_degree': forms.Select(),
            'with_fourth_degree': forms.Select(),
            'offense': forms.Select(),
            'criminal': forms.Select(),
            'convicted': forms.Select(),
            'sep_service': forms.Select(),
            'candidate': forms.Select(),
            'resign_candid': forms.Select(),
            'immigrant_status': forms.Select(),
            'indigenous_group_member': forms.Select(),
            'disability_status': forms.Select(),
            'solo_parent_status': forms.Select(),
            'criminal_date': forms.DateInput(attrs={'type': 'date'}),
            'date_accomplished': forms.DateInput(attrs={'type': 'date'}),
            'id_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'references': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter references, separated by commas or new lines'}),

        }


class EducationalBackgroundForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'elementary_name': forms.TextInput(attrs={'placeholder': 'Name of Elementary School'}),
            'elementary_period_from': forms.TextInput(attrs={'placeholder': 'YYYY'}),
            'elementary_period_to': forms.TextInput(attrs={'placeholder': 'YYYY'}),
            'secondary_name': forms.TextInput(attrs={'placeholder': 'Name of Secondary School'}),
            'secondary_period_from': forms.TextInput(attrs={'placeholder': 'YYYY'}),

            'vocational_period_to': forms.TextInput(attrs={'placeholder': 'YYYY'}),
            'vocational_period_from': forms.TextInput(attrs={'placeholder': 'YYYY'}),

            'college_period_to': forms.TextInput(attrs={'placeholder': 'YYYY'}),
            'college_period_from': forms.TextInput(attrs={'placeholder': 'YYYY'}),

            'graduate_period_to': forms.TextInput(attrs={'placeholder': 'YYYY'}),
            'graduate_period_from': forms.TextInput(attrs={'placeholder': 'YYYY'}),

            'secondary_period_to': forms.TextInput(attrs={'placeholder': 'YYYY'}),
            'vocational_name': forms.TextInput(attrs={'placeholder': 'Name of Vocational/Trade School'}),
            'college_name': forms.TextInput(attrs={'placeholder': 'Name of College'}),
            'graduate_name': forms.TextInput(attrs={'placeholder': 'Name of Graduate School'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # # Make all fields required
        # for field_name, field in self.fields.items():
        #     field.required = True
        #     # Optionally, add 'required' attribute to widgets for frontend validation
        #     if hasattr(field.widget.attrs, 'required'):
        #         field.widget.attrs['required'] = 'required'
        pass

class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.Select(),
            'civil_status': forms.Select(),
            'blood_type': forms.Select(),
            'residential_address': forms.Textarea(attrs={'rows': 3}),
            'permanent_address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'sss_no': 'SSS Number',
            'tin_no': 'TIN Number',
            'email_address': 'Email Address (optional)',
            'residential_zip_code': 'Residential Zip Code',
            'permanent_zip_code': 'Permanent Zip Code',
        }


class FamilyBackgroundForm(forms.ModelForm):
    class Meta:
        model = FamilyBackground
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'spouse_business_address': forms.Textarea(attrs={'rows': 3}),
            'children': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter children names, separated by commas or new lines'}),
        }
        labels = {
            'spouse_surname': "Spouse's Surname",
            'spouse_firstname': "Spouse's First Name",
            'spouse_middlename': "Spouse's Middle Name",
            'spouse_name_extension': "Spouse's Name Extension",
            'spouse_employer_business_name': "Employer/Business Name",
            'spouse_business_address': "Business Address",
            'father_surname': "Father's Surname",
            'father_firstname': "Father's First Name",
            'father_middlename': "Father's Middle Name",
            'father_name_extension': "Father's Name Extension",
            'mother_maiden_lastname': "Mother's Maiden Last Name",
            'mother_firstname': "Mother's First Name",
            'mother_middlename': "Mother's Middle Name",
        }

