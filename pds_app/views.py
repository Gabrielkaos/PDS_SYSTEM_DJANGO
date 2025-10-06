from django.shortcuts import render, redirect
from .models import *
from .forms import PersonalInformationForm, FamilyBackgroundForm, EducationalBackgroundForm, OtherInformationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


SECTIONS = {
    'personal_info': {
        'template': 'pds_app/personal_information.html',
        'form': PersonalInformationForm,
        'name':'Personal Information'
    },
    'family_background': {
        'template': 'pds_app/family_background.html',
        'form': FamilyBackgroundForm,
        'name':'Family Background'
    },
    'educational_background': {
        'template': 'pds_app/educational_background.html',
        'form': EducationalBackgroundForm,
        'name':'Educational Background'
    },
    'civil_service_eligibility': {
        'template': 'pds_app/civil_service_eligibility.html',
        'form': None,
        'name':'Civil Service Eligibility'
    },
    'work_experience': {
        'template': 'pds_app/work_experience.html',
        'form': None,
        'name':'Work Experience'
    },
    'voluntary_work': {
        'template': 'pds_app/voluntary_work.html',
        'form': None,
        'name':'Voluntary Work'
    },
    'learning_and_development': {
        'template': 'pds_app/learning_and_development.html',
        'form': None,
        'name':'Learning and Development'
    },
    'other_information': {
        'template': 'pds_app/other_information.html',
        'form': OtherInformationForm,
        'name':'Other Information'
    },
}


from django.shortcuts import redirect, get_object_or_404




# def section_view(request, section):
    
#     if section not in SECTIONS:
#         return redirect('section_view', section='personal_info')
    
#     section_details = SECTIONS[section]
#     form_class = section_details['form']
#     section_name = section_details['name']
#     form = form_class(request.POST or None) if form_class else None

#     # latest_form = FormID.objects.get(name=get_latest_form_number(FormID.objects.all()))

#     if request.method == 'POST':
#         if form:
#             if form.is_valid():
#                 form1 = form.save(commit=False)
#                 form1.save()
#                 print(section_name,"Saved!")
#             else:
#                 print(section_name,"Not Valid!")
#         else:
#             if section == 'civil_service_eligibility':
#                 career_services = request.POST.getlist('career_service[]')
#                 ratings = request.POST.getlist('rating[]')
#                 exam_dates = request.POST.getlist('exam_date[]')
#                 exam_places = request.POST.getlist('exam_place[]')
#                 license_numbers = request.POST.getlist('license_number[]')
#                 license_validities = request.POST.getlist('license_validity[]')
#                 latest_name = get_latest_name(CivilServiceEligibility)

#                 print(len(career_services))


#                 # Loop through each entry and save
#                 for i in range(len(career_services)):
#                     career_service = career_services[i]
#                     rating = ratings[i] if i < len(ratings) else None
#                     exam_date = exam_dates[i] if i < len(exam_dates) else None
#                     exam_place = exam_places[i]
#                     license_number = license_numbers[i]
#                     license_validity = license_validities[i] if i < len(license_validities) else None

#                     civil_service_eligibility = CivilServiceEligibility.objects.create(
#                         name = str(latest_name + 1),
#                         career_service=career_service,
#                         rating=rating,
#                         exam_date=exam_date,
#                         exam_place=exam_place,
#                         license_number=license_number,
#                         license_validity=license_validity,
#                     )
#                     civil_service_eligibility.save()
#                 print("Civil Service Eligibility Saved!")

#             elif section == 'voluntary_work':
#                 organization_names = request.POST.getlist('organization_name[]')
#                 from_dates = request.POST.getlist('from_date[]')
#                 to_dates = request.POST.getlist('to_date[]')
#                 number_of_hours = request.POST.getlist('number_of_hours[]')
#                 nature_of_works = request.POST.getlist('nature_of_work[]')
#                 latest_name = get_latest_name(VoluntaryWork)

#                 # Loop through each entry and save
#                 for i in range(len(organization_names)):
#                     organization_name = organization_names[i]
#                     from_date = from_dates[i] if i < len(from_dates) else None
#                     to_date = to_dates[i] if i < len(to_dates) else None
#                     number_of_hour = number_of_hours[i] if i < len(number_of_hours) else None
#                     nature_of_work = nature_of_works[i]

#                     voluntary_work = VoluntaryWork.objects.create(
#                         name = str(latest_name + 1),
#                         organization_name=organization_name,
#                         from_date=from_date,
#                         to_date=to_date,
#                         number_of_hours=number_of_hour,
#                         nature_of_work=nature_of_work,
#                     )
#                     voluntary_work.save()
#                 print("Voluntary Work Saved!")

#             elif section == 'learning_and_development':
#                 titles = request.POST.getlist('title[]')
#                 from_dates = request.POST.getlist('from_date[]')
#                 to_dates = request.POST.getlist('to_date[]')
#                 number_of_hours = request.POST.getlist('number_of_hours[]')
#                 types_of_ld = request.POST.getlist('type_of_ld[]')
#                 conducted_bys = request.POST.getlist('conducted_by[]')
#                 latest_name = get_latest_name(LearningDevelopment)

#                 # Loop through each entry and save
#                 for i in range(len(titles)):
#                     title = titles[i]
#                     from_date = from_dates[i] if i < len(from_dates) else None
#                     to_date = to_dates[i] if i < len(to_dates) else None
#                     number_of_hour = number_of_hours[i] if i < len(number_of_hours) else None
#                     type_of_ld = types_of_ld[i]
#                     conducted_by = conducted_bys[i]

#                     learning_development = LearningDevelopment.objects.create(
#                         name = str(latest_name + 1),
#                         title=title,
#                         from_date=from_date,
#                         to_date=to_date,
#                         number_of_hours=number_of_hour,
#                         type_of_ld=type_of_ld,
#                         conducted_by=conducted_by,
#                     )
#                     learning_development.save()
#                 print("Learning and Development Saved!")

#             elif section == 'work_experience':
#                 from_dates = request.POST.getlist('from_date[]')
#                 to_dates = request.POST.getlist('to_date[]')
#                 position_titles = request.POST.getlist('position_title[]')
#                 departments = request.POST.getlist('department[]')
#                 monthly_salaries = request.POST.getlist('monthly_salary[]')
#                 salary_grades = request.POST.getlist('salary_grade[]')
#                 status_of_appointments = request.POST.getlist('status_of_appointment[]')
#                 govt_services = request.POST.getlist('govt_service[]')
#                 latest_name = get_latest_name(WorkExperience)

#                 for i in range(len(from_dates)):
#                     from_date = from_dates[i] if i < len(from_dates) else None
#                     to_date = to_dates[i] if i < len(to_dates) else None
#                     position_title = position_titles[i] if i < len(position_titles) else ''
#                     department = departments[i] if i < len(departments) else ''
#                     monthly_salary = monthly_salaries[i] if i < len(monthly_salaries) else None
#                     salary_grade = salary_grades[i] if i < len(salary_grades) else None
#                     status_of_appointment = status_of_appointments[i] if i < len(status_of_appointments) else ''
#                     govt_service = govt_services[i] if i < len(govt_services) else 'N'  # Default to 'N' if not selected

#                     work_experience = WorkExperience.objects.create(
#                         name = str(latest_name + 1),
#                         from_date=from_date,
#                         to_date=to_date,
#                         position_title=position_title,
#                         department=department,
#                         monthly_salary=monthly_salary,
#                         salary_grade=salary_grade,
#                         status_of_appointment=status_of_appointment,
#                         govt_service=govt_service,
#                     )
#                     work_experience.save()
#                 print("Work Experience Saved!")

            

            
#         sections_list = list(SECTIONS.keys())
#         current_index = sections_list.index(section)
#         if current_index + 1 < len(sections_list):
#             next_section = sections_list[current_index + 1]
#             return redirect('section_view', section=next_section)
#         else:
            
#             personal_info = get_latest(PersonalInformation)
#             other_info = get_latest(OtherInformation)
#             family = get_latest(FamilyBackground)
#             education = get_latest(EducationalBackground)

#             work = get_latest_objects(WorkExperience)
#             learning = get_latest_objects(LearningDevelopment)
#             civil = get_latest_objects(CivilServiceEligibility)
#             voluntary = get_latest_objects(VoluntaryWork)

#             complete_form = CompleteForm.objects.create(
#                 name=request.POST['form_name'],
#                 other_information=other_info,
#                 educational_background=education,
#                 personal_information = personal_info,
#                 family_background = family,
#             )

#             complete_form.voluntary_work.set(voluntary)
#             complete_form.civil_service.set(civil)
#             complete_form.learning_development.set(learning)
#             complete_form.work_experience.set(work)

#             complete_form.save()
#             return redirect("/")

#     context = {
#         'active_section': section,
#         'form': form,
#         'SECTIONS': SECTIONS
#     }

#     return render(request, section_details['template'], context)


def section_view(request, section):
    if section not in SECTIONS:
        return redirect('section_view', section='personal_info')
    
    section_details = SECTIONS[section]
    print(section_details)
    
    if request.method == 'POST':
        print("Hello")
        return handle_section_post(request, section, section_details)
    
    form_class = section_details['form']
    context = {
        'active_section': section,
        'form': form_class(request.POST or None) if form_class else None,
        'SECTIONS': SECTIONS
    }
    return render(request, section_details['template'], context)

def handle_section_post(request, section, section_details):
    """Handle POST requests for each section"""
    form_class = section_details['form']
    
    if form_class:
        return handle_form_section(request, section, form_class)
    else:
        return handle_dynamic_section(request, section)
    

def handle_form_section(request, section, form_class):
    """Handle sections with Django forms"""
    form = form_class(request.POST)
    if form.is_valid():
        form_instance = form.save(commit=False)
        form_instance.user = request.user
        form_instance.save()
        return get_next_section_redirect(request, section)
    else:
        # Pass the invalid form back to the context
        print("Form errors:", form.errors)
        print("Non-field errors:", form.non_field_errors())
        
        # Print each field's errors
        for field in form:
            if field.errors:
                print(f"Field '{field.name}' errors: {field.errors}")
        messages.error(request, "Please correct the errors below.")
        context = get_section_context(request, section, form)  # Pass the form here
        return render(request, SECTIONS[section]['template'], context)

def get_section_context(request, section, form=None):
    """Get context for section templates"""
    section_details = SECTIONS[section]
    
    # If it's a GET request and we have existing data, pre-populate the form
    if form is None and section_details['form'] and request.method == 'GET':
        try:
            # Get the form class from SECTIONS
            form_class = section_details['form']
            # Get the model from the form's Meta class
            model_class = form_class.Meta.model
            # Get latest instance for this user
            latest_instance = get_user_latest(model_class, request.user)
            if latest_instance:
                form = form_class(instance=latest_instance)
            else:
                form = form_class()
        except Exception as e:
            print(f"Error pre-populating form: {e}")
            form = form_class()
    
    return {
        'active_section': section,
        'form': form,
        'SECTIONS': SECTIONS,
        'section_name': section_details['name']
    }

def handle_dynamic_section(request, section):
    """Handle sections without Django forms (civil service, work experience, etc.)"""
    handlers = {
        'civil_service_eligibility': handle_civil_service,
        'voluntary_work': handle_voluntary_work,
        'learning_and_development': handle_learning_and_development,
        'work_experience': handle_work_experience,
    }
    
    handler = handlers.get(section)
    if handler:
        handler(request)
        return get_next_section_redirect(request, section)
    
    return redirect('section_view', section=section)

def get_next_section_redirect(request, current_section):
    """Get the next section in the workflow"""
    sections_list = list(SECTIONS.keys())
    current_index = sections_list.index(current_section)
    
    if current_index + 1 < len(sections_list):
        next_section = sections_list[current_index + 1]
        return redirect('section_view', section=next_section)
    else:
        return handle_final_submission(request)
    

def handle_final_submission(request):
    """Handle the final form submission"""
    try:
        # Get the latest entries for this user
        personal_info = PersonalInformation.objects.filter(user=request.user).latest('id')
        other_info = OtherInformation.objects.filter(user=request.user).latest('id')
        family_background = FamilyBackground.objects.filter(user=request.user).latest('id')
        educational_background = EducationalBackground.objects.filter(user=request.user).latest('id')

        # Get related ManyToMany objects for this user
        work_experiences = WorkExperience.objects.filter(user=request.user)
        learning_developments = LearningDevelopment.objects.filter(user=request.user)
        civil_services = CivilServiceEligibility.objects.filter(user=request.user)
        voluntary_works = VoluntaryWork.objects.filter(user=request.user)

        # Create complete form
        complete_form = CompleteForm.objects.create(
            user=request.user,
            name=request.POST.get('form_name', f'Form {request.user.username}'),
            personal_information=personal_info,
            other_information=other_info,
            family_background=family_background,
            educational_background=educational_background,
        )

        # Set ManyToMany relationships
        complete_form.work_experience.set(work_experiences)
        complete_form.learning_development.set(learning_developments)
        complete_form.civil_service.set(civil_services)
        complete_form.voluntary_work.set(voluntary_works)

        return redirect('forms')
    
    except Exception as e:
        print(f"Error creating complete form: {e}")
        # Handle error appropriately
        return redirect('section_view', section='personal_info')
    
def handle_civil_service(request):
    """Handle civil service eligibility submission"""
    try:
        career_services = request.POST.getlist('career_service[]')
        
        for i in range(len(career_services)):
            CivilServiceEligibility.objects.create(
                user=request.user,
                career_service=career_services[i],
                rating=request.POST.getlist('rating[]')[i] if i < len(request.POST.getlist('rating[]')) else None,
                exam_date=request.POST.getlist('exam_date[]')[i] if i < len(request.POST.getlist('exam_date[]')) else None,
                exam_place=request.POST.getlist('exam_place[]')[i],
                license_number=request.POST.getlist('license_number[]')[i],
                license_validity=request.POST.getlist('license_validity[]')[i] if i < len(request.POST.getlist('license_validity[]')) else None,
            )
        return True
    except Exception as e:
        print(f"Error saving civil service: {e}")
        return False
    
def handle_voluntary_work(request):
    """Handle voluntary work submission"""
    try:
        organization_names = request.POST.getlist('organization_name[]')
        
        for i in range(len(organization_names)):
            if organization_names[i].strip():  # Only save if not empty
                VoluntaryWork.objects.create(
                    user=request.user,
                    organization_name=organization_names[i],
                    from_date=request.POST.getlist('from_date[]')[i] if i < len(request.POST.getlist('from_date[]')) and request.POST.getlist('from_date[]')[i] else None,
                    to_date=request.POST.getlist('to_date[]')[i] if i < len(request.POST.getlist('to_date[]')) and request.POST.getlist('to_date[]')[i] else None,
                    number_of_hours=request.POST.getlist('number_of_hours[]')[i] if i < len(request.POST.getlist('number_of_hours[]')) and request.POST.getlist('number_of_hours[]')[i] else 0,
                    nature_of_work=request.POST.getlist('nature_of_work[]')[i] if i < len(request.POST.getlist('nature_of_work[]')) else '',
                )
        # messages.success(request, "Voluntary Work saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving voluntary work: {e}")
        # messages.error(request, "Error saving Voluntary Work. Please try again.")
        return False

def handle_learning_and_development(request):
    """Handle learning and development submission"""
    try:
        titles = request.POST.getlist('title[]')
        
        for i in range(len(titles)):
            if titles[i].strip():  # Only save if not empty
                LearningDevelopment.objects.create(
                    user=request.user,
                    title=titles[i],
                    from_date=request.POST.getlist('from_date[]')[i] if i < len(request.POST.getlist('from_date[]')) and request.POST.getlist('from_date[]')[i] else None,
                    to_date=request.POST.getlist('to_date[]')[i] if i < len(request.POST.getlist('to_date[]')) and request.POST.getlist('to_date[]')[i] else None,
                    number_of_hours=request.POST.getlist('number_of_hours[]')[i] if i < len(request.POST.getlist('number_of_hours[]')) and request.POST.getlist('number_of_hours[]')[i] else 0,
                    type_of_ld=request.POST.getlist('type_of_ld[]')[i] if i < len(request.POST.getlist('type_of_ld[]')) else '',
                    conducted_by=request.POST.getlist('conducted_by[]')[i] if i < len(request.POST.getlist('conducted_by[]')) else '',
                )
        # messages.success(request, "Learning and Development saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving learning and development: {e}")
        # messages.error(request, "Error saving Learning and Development. Please try again.")
        return False

def handle_work_experience(request):
    """Handle work experience submission"""
    try:
        from_dates = request.POST.getlist('from_date[]')
        
        for i in range(len(from_dates)):
            WorkExperience.objects.create(
                user=request.user,
                from_date=from_dates[i],
                to_date=request.POST.getlist('to_date[]')[i] if i < len(request.POST.getlist('to_date[]')) else None,
                position_title=request.POST.getlist('position_title[]')[i] if i < len(request.POST.getlist('position_title[]')) else '',
                department=request.POST.getlist('department[]')[i] if i < len(request.POST.getlist('department[]')) else '',
                monthly_salary=request.POST.getlist('monthly_salary[]')[i] if i < len(request.POST.getlist('monthly_salary[]')) else None,
                salary_grade=request.POST.getlist('salary_grade[]')[i] if i < len(request.POST.getlist('salary_grade[]')) else None,
                status_of_appointment=request.POST.getlist('status_of_appointment[]')[i] if i < len(request.POST.getlist('status_of_appointment[]')) else '',
                govt_service=request.POST.getlist('govt_service[]')[i] if i < len(request.POST.getlist('govt_service[]')) else 'N',
            )
        return True
    except Exception as e:
        print(f"Error saving work experience: {e}")
        return False

def get_user_latest(cls, user):
    """Get latest object for a specific user"""
    try:
        return cls.objects.filter(user=user).latest('id')
    except cls.DoesNotExist:
        return None

def get_user_objects(cls, user):
    """Get all objects for a specific user"""
    return cls.objects.filter(user=user)




def get_latest(cls):
    
    return cls.objects.latest('id')


def get_latest_name(cls):
    
    civil = cls.objects.all()

    if len(civil)==0:
        return 0
    numbers = []
    for civ in civil:
        numbers.append(int(civ.name))

    numbers.sort()

    return numbers[-1]


def get_latest_objects(cls):
    
    civil = cls.objects.all()

    only = []

    for civ in civil:
        if int(civ.name) == get_latest_name(cls):
            only.append(civ)
    
    return only

@login_required
def home(request):
    forms1 = CompleteForm.objects.filter(user=request.user)
    return render(request, "pds_app/forms.html", {"forms": forms1})
    # forms1 = CompleteForm.objects.all()
    # return render(request,"pds_app/forms.html",{"forms":forms1})

@login_required
def create_form(request):
    return redirect('section_view', section='personal_info')

@login_required
def all_forms(request, form_id):
    """View specific form - ensure user can only see their own forms"""
    form_instance = get_object_or_404(CompleteForm, id=form_id, user=request.user)
    user_forms = CompleteForm.objects.filter(user=request.user)
    
    return render(request, "pds_app/all_forms.html", {
        "form": form_instance, 
        "forms": user_forms
    })

@login_required
def forms(request):
    """Show only user's forms"""
    user_forms = CompleteForm.objects.filter(user=request.user)
    return render(request, "pds_app/forms.html", {"forms": user_forms})


def delete_form(request, form_id):
    """Ensure users can only delete their own forms"""
    form = get_object_or_404(CompleteForm, id=form_id, user=request.user)
    
    if request.method == "POST":
        form.delete()
        return redirect('forms')
    
    return redirect('forms')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')