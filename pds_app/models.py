from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class PersonalInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_informations")

    # form_id = models.ForeignKey(FormID, on_delete=models.CASCADE)
    
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)

    
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)

    
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    civil_status = models.CharField(max_length=15, choices=[
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated')
    ])
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(50), MaxValueValidator(300)],  # reasonable range in cm
        help_text="Height in cm"
    )
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(20), MaxValueValidator(300)],  # reasonable range in kg
        help_text="Weight in kg"
    )
    blood_type = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), 
        ('O+', 'O+'), ('O-', 'O-')
    ])

    
    gsis = models.CharField(max_length=50, blank=True, null=True)
    pag_ibig = models.CharField(max_length=50, blank=True, null=True)
    philhealth = models.CharField(max_length=50, blank=True, null=True)
    sss_no = models.CharField(max_length=50, blank=True, null=True)
    tin_no = models.CharField(max_length=50, blank=True, null=True)

    
    agent_employee_number = models.CharField(max_length=50, blank=True, null=True)

    
    citizenship = models.CharField(max_length=50)

    
    residential_address = models.TextField()
    residential_zip_code = models.CharField(max_length=10)
    permanent_address = models.TextField(blank=True, null=True)
    permanent_zip_code = models.CharField(max_length=10, blank=True, null=True)

    
    telephone_no = models.CharField(max_length=15, blank=True, null=True)
    mobile_no = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    email_address = models.EmailField(blank=True, null=True)

    @property
    def full_name(self):
        """Return full name"""
        if self.middlename:
            return f"{self.firstname} {self.middlename} {self.surname}"
        return f"{self.firstname} {self.surname}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    

    def __str__(self):
        return f"{self.firstname} {self.middlename or ''} {self.surname}"

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
        indexes = [
            models.Index(fields=['surname', 'firstname']),
            models.Index(fields=['agent_employee_number']),
            models.Index(fields=['email_address']),
        ]


class FamilyBackground(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="family_backgrounds")
   
    spouse_surname = models.CharField(max_length=100, blank=True, null=True)
    spouse_firstname = models.CharField(max_length=100, blank=True, null=True)
    spouse_middlename = models.CharField(max_length=100, blank=True, null=True)
    spouse_name_extension = models.CharField(max_length=10, blank=True, null=True, help_text="e.g., Jr., Sr., III")
    spouse_occupation = models.CharField(max_length=100, blank=True, null=True)
    spouse_employer_business_name = models.CharField(max_length=255, blank=True, null=True)
    spouse_business_address = models.TextField(blank=True, null=True)
    spouse_telephone_no = models.CharField(max_length=15, blank=True, null=True)

   
    children = models.TextField(blank=True, null=True, verbose_name='Children (Enter names separated by commas or new lines)')

    
    father_surname = models.CharField(max_length=100)
    father_firstname = models.CharField(max_length=100)
    father_middlename = models.CharField(max_length=100, blank=True, null=True)
    father_name_extension = models.CharField(max_length=10, blank=True, null=True, help_text="e.g., Jr., Sr., III")

    
    mother_maiden_lastname = models.CharField(max_length=100)
    mother_firstname = models.CharField(max_length=100)
    mother_middlename = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Family Background of {self.spouse_surname or 'N/A'}"

    class Meta:
        verbose_name = "Family Background"
        verbose_name_plural = "Family Backgrounds"


class VoluntaryWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="voluntary_works")

    # form_id = models.ForeignKey(FormID, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)

    organization_name = models.CharField(max_length=255, verbose_name="Name and Address of Organization (Write in Full)",null=True,blank=True)
    from_date = models.DateField(verbose_name="Inclusive Dates (From)",null=True,blank=True)
    to_date = models.DateField(verbose_name="Inclusive Dates (To)",null=True,blank=True)
    number_of_hours = models.PositiveIntegerField(verbose_name="Number of Hours",null=True,blank=True)
    nature_of_work = models.CharField(max_length=255, verbose_name="Position/Nature of Work",null=True,blank=True)

    def __str__(self):
        return f"{self.organization_name} ({self.nature_of_work})"

    class Meta:
        verbose_name = "Voluntary Work"
        verbose_name_plural = "Voluntary Works"
        ordering = ['-from_date']

class LearningDevelopment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="learning_developments")

    # form_id = models.ForeignKey(FormID, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)

    title = models.CharField(max_length=255, verbose_name="Title of Learning and Development Interventions/Training Programs (Write in Full)",blank=True,null=True)
    from_date = models.DateField(verbose_name="Inclusive Dates (From)",blank=True,null=True)
    to_date = models.DateField(verbose_name="Inclusive Dates (To)",blank=True,null=True)
    number_of_hours = models.PositiveIntegerField(verbose_name="Number of Hours",blank=True,null=True)
    type_of_ld = models.CharField(max_length=100, verbose_name="Type of LD (Managerial/Supervisory/Technical, etc.)",blank=True,null=True)
    conducted_by = models.CharField(max_length=255, verbose_name="Conducted/Sponsored By (Write in Full)",blank=True,null=True)

    def __str__(self):
        return f"{self.title} ({self.type_of_ld})"

    class Meta:
        verbose_name = "Learning and Development"
        verbose_name_plural = "Learning and Development"

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_experiences")

    # form_id = models.ForeignKey(FormID, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)

    from_date = models.DateField(verbose_name="Inclusive Dates (From)",blank=True,null=True)
    to_date = models.DateField(verbose_name="Inclusive Dates (To)",blank=True,null=True)
    position_title = models.CharField(max_length=255, verbose_name="Position Title (Write in Full)",blank=True,null=True)
    department = models.CharField(
        max_length=255,
        verbose_name="Department/Agency/Office/Company (Write in Full)",blank=True,null=True
    )
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monthly Salary",blank=True,null=True)
    salary_grade = models.CharField(
        max_length=10, blank=True, null=True,
        verbose_name="Salary/Job/Pay Grade & STEP (Format '00-0')/Increment"
    )
    status_of_appointment = models.CharField(max_length=255, verbose_name="Status of Appointment",blank=True,null=True)
    govt_service = models.CharField(
        max_length=3, choices=[('Y', 'Yes'), ('N', 'No')],
        verbose_name="Government Service (Y/N)",blank=True,null=True
    )

    def __str__(self):
        
        return f"{self.position_title} - {self.department}"

    @property
    def duration_years(self):
        """Calculate duration in years"""
        from datetime import date
        if self.to_date:
            delta = self.to_date - self.from_date
            return delta.days / 365.25
        return (date.today() - self.from_date).days / 365.25

    class Meta:
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"
        ordering = ['-from_date']  
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.to_date and self.from_date > self.to_date:
            raise ValidationError("End date cannot be before start date")


class OtherInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="other_informations")
    # Relatives by consanguinity or affinity
    with_third_degree = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Within Third Degree (Y/N)"
    )
    with_fourth_degree = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Within Fourth Degree (Y/N)"
    )
    fourth_degree_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details for Fourth Degree (if any)"
    )

    # Administrative and Criminal Offenses
    offense = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Administrative Offense (Y/N)"
    )
    offense_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Administrative Offense"
    )
    criminal = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Criminally Charged (Y/N)"
    )
    criminal_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Criminal Charge"
    )
    criminal_date = models.DateField(
        null=True, blank=True, 
        verbose_name="Date of Criminal Charge"
    )

    # Conviction
    convicted = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Convicted of Crime (Y/N)"
    )
    convicted_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Conviction"
    )

    # Service Separation
    sep_service = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Separated from Service (Y/N)"
    )
    sep_service_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Service Separation"
    )

    # Election-Related Questions
    candidate = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Candidate in Election (Y/N)"
    )
    candidate_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Election Candidacy"
    )
    resign_candid = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Resigned for Election Campaign (Y/N)"
    )
    resign_candid_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Election Campaign Resignation"
    )

    # Immigration or Permanent Residency
    immigrant_status = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Immigrant/Permanent Resident Status (Y/N)"
    )
    immigrant_details = models.TextField(
        max_length=200, blank=True, null=True, 
        verbose_name="Details of Immigration Status"
    )

    # Membership and Other Information
    indigenous_group_member = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Member of Indigenous Group (Y/N)"
    )
    disability_status = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Person with Disability (Y/N)"
    )
    solo_parent_status = models.CharField(
        max_length=3, 
        default='N',
        choices=[('Y', 'Yes'), ('N', 'No')], 
        verbose_name="Solo Parent (Y/N)"
    )

    # References
    references = models.TextField(blank=True, null=True, verbose_name='References (Enter details separated by new lines or commas)')


    # Government Issued ID
    government_id = models.CharField(
        max_length=50,null=True, blank=True,  
        verbose_name="Government Issued ID"
    )
    government_id_number = models.CharField(
        max_length=100, null=True, blank=True, 
        verbose_name="ID/License/Passport Number"
    )
    id_issue_date = models.DateField(
        null=True, blank=True, 
        verbose_name="ID Issue Date"
    )
    id_issue_place = models.CharField(
        max_length=100, null=True, blank=True, 
        verbose_name="ID Issue Place"
    )

    # Final Details
    date_accomplished = models.DateField(
        auto_now_add=True, 
        verbose_name="Date Accomplished"
    )

    def __str__(self):
        return f"Other Information for {self.id}"



class CivilServiceEligibility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="civil_service_eligibilities")

    # form_id = models.ForeignKey(FormID, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)

    career_service = models.CharField(
        max_length=255,null=True,blank=True,
        verbose_name="Career Service/RA 1080 (Board/Bar) under Special Laws/CES/CSEE/Barangay Eligibility/Driver's License"
    )
    rating = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Rating (if applicable)"
    )
    exam_date = models.DateField(verbose_name="Date of Examination/Conferment",null=True,blank=True)
    exam_place = models.CharField(max_length=255, verbose_name="Place of Examination/Conferment",null=True,blank=True)
    license_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="License Number (if applicable)")
    license_validity = models.DateField(blank=True, null=True, verbose_name="License Validity (if applicable)")

    def __str__(self):
        return f"{self.career_service} - {self.exam_date}"

    class Meta:
        verbose_name = "Civil Service Eligibility"
        verbose_name_plural = "Civil Service Eligibilities"

class EducationalBackground(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educational_backgrounds")
    # name = models.CharField(max_length=255)


    # form_id = models.ForeignKey(FormID, on_delete=models.CASCADE)

    elementary_name = models.CharField(max_length=255, verbose_name="Elementary - Name of School")
    elementary_degree_course = models.CharField(max_length=255, blank=True, null=True, verbose_name="Elementary - Basic Ed/Degree/Course")
    elementary_period_from = models.CharField(max_length=4, verbose_name="Elementary - Period of Attendance (From)")
    elementary_period_to = models.CharField(max_length=4, verbose_name="Elementary - Period of Attendance (To)")
    elementary_highest_level_units = models.CharField(max_length=255, blank=True, null=True, verbose_name="Elementary - Highest Level/Units Earned")
    elementary_year_graduated = models.CharField(max_length=4, blank=True, null=True, verbose_name="Elementary - Year Graduated")
    elementary_honors = models.CharField(max_length=255, blank=True, null=True, verbose_name="Elementary - Scholarship/Honors Received")

    secondary_name = models.CharField(max_length=255, verbose_name="Secondary - Name of School")
    secondary_degree_course = models.CharField(max_length=255, blank=True, null=True, verbose_name="Secondary - Basic Ed/Degree/Course")
    secondary_period_from = models.CharField(max_length=4, verbose_name="Secondary - Period of Attendance (From)")
    secondary_period_to = models.CharField(max_length=4, verbose_name="Secondary - Period of Attendance (To)")
    secondary_highest_level_units = models.CharField(max_length=255, blank=True, null=True, verbose_name="Secondary - Highest Level/Units Earned")
    secondary_year_graduated = models.CharField(max_length=4, blank=True, null=True, verbose_name="Secondary - Year Graduated")
    secondary_honors = models.CharField(max_length=255, blank=True, null=True, verbose_name="Secondary - Scholarship/Honors Received")

    vocational_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vocational/Trade Course - Name of School")
    vocational_degree_course = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vocational/Trade Course - Basic Ed/Degree/Course")
    vocational_period_from = models.CharField(max_length=4, blank=True, null=True, verbose_name="Vocational/Trade Course - Period of Attendance (From)")
    vocational_period_to = models.CharField(max_length=4, blank=True, null=True, verbose_name="Vocational/Trade Course - Period of Attendance (To)")
    vocational_highest_level_units = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vocational/Trade Course - Highest Level/Units Earned")
    vocational_year_graduated = models.CharField(max_length=4, blank=True, null=True, verbose_name="Vocational/Trade Course - Year Graduated")
    vocational_honors = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vocational/Trade Course - Scholarship/Honors Received")

    college_name = models.CharField(max_length=255, verbose_name="College - Name of School")
    college_degree_course = models.CharField(max_length=255, blank=True, null=True, verbose_name="College - Basic Ed/Degree/Course")
    college_period_from = models.CharField(max_length=4, verbose_name="College - Period of Attendance (From)")
    college_period_to = models.CharField(max_length=4, verbose_name="College - Period of Attendance (To)")
    college_highest_level_units = models.CharField(max_length=255, blank=True, null=True, verbose_name="College - Highest Level/Units Earned")
    college_year_graduated = models.CharField(max_length=4, blank=True, null=True, verbose_name="College - Year Graduated")
    college_honors = models.CharField(max_length=255, blank=True, null=True, verbose_name="College - Scholarship/Honors Received")

    graduate_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Graduate Studies - Name of School")
    graduate_degree_course = models.CharField(max_length=255, blank=True, null=True, verbose_name="Graduate Studies - Basic Ed/Degree/Course")
    graduate_period_from = models.CharField(max_length=4, blank=True, null=True, verbose_name="Graduate Studies - Period of Attendance (From)")
    graduate_period_to = models.CharField(max_length=4, blank=True, null=True, verbose_name="Graduate Studies - Period of Attendance (To)")
    graduate_highest_level_units = models.CharField(max_length=255, blank=True, null=True, verbose_name="Graduate Studies - Highest Level/Units Earned")
    graduate_year_graduated = models.CharField(max_length=4, blank=True, null=True, verbose_name="Graduate Studies - Year Graduated")
    graduate_honors = models.CharField(max_length=255, blank=True, null=True, verbose_name="Graduate Studies - Scholarship/Honors Received")

    def __str__(self):
        return f"Educational Background Record"

    class Meta:
        verbose_name = "Educational Background"
        verbose_name_plural = "Educational Backgrounds"


class CompleteForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms")
    # name = models.CharField(max_length=200)
    
    # Make foreign keys optional for flexibility
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, null=True, blank=True)
    family_background = models.ForeignKey(FamilyBackground, on_delete=models.CASCADE, null=True, blank=True)
    educational_background = models.ForeignKey(EducationalBackground, on_delete=models.CASCADE, null=True, blank=True)
    other_information = models.ForeignKey(OtherInformation, on_delete=models.CASCADE, null=True, blank=True)
    
    # ManyToMany relationships are fine as is
    voluntary_work = models.ManyToManyField(VoluntaryWork, blank=True)
    learning_development = models.ManyToManyField(LearningDevelopment, blank=True)
    work_experience = models.ManyToManyField(WorkExperience, blank=True)
    civil_service = models.ManyToManyField(CivilServiceEligibility, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"
    
    @property
    def name(self):
        return f"{self.personal_information.full_name}"

    class Meta:
        ordering = ['-created_at']