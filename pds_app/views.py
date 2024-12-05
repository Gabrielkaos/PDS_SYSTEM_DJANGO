from django.shortcuts import render, redirect
from .models import *
from .forms import PersonalInformationForm, FamilyBackgroundForm, EducationalBackgroundForm, OtherInformationForm

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


def section_view(request, section):
    
    if section not in SECTIONS:
        return redirect('section_view', section='personal_info')
    
    section_details = SECTIONS[section]
    form_class = section_details['form']
    section_name = section_details['name']
    form = form_class(request.POST or None) if form_class else None

    # latest_form = FormID.objects.get(name=get_latest_form_number(FormID.objects.all()))

    if request.method == 'POST':
        if form:
            if form.is_valid():
                form1 = form.save(commit=False)
                form1.save()
                print(section_name,"Saved!")
            else:
                print(section_name,"Not Valid!")
        else:
            if section == 'civil_service_eligibility':
                career_services = request.POST.getlist('career_service[]')
                ratings = request.POST.getlist('rating[]')
                exam_dates = request.POST.getlist('exam_date[]')
                exam_places = request.POST.getlist('exam_place[]')
                license_numbers = request.POST.getlist('license_number[]')
                license_validities = request.POST.getlist('license_validity[]')
                latest_name = get_latest_name(CivilServiceEligibility)

                print(len(career_services))


                # Loop through each entry and save
                for i in range(len(career_services)):
                    career_service = career_services[i]
                    rating = ratings[i] if i < len(ratings) else None
                    exam_date = exam_dates[i] if i < len(exam_dates) else None
                    exam_place = exam_places[i]
                    license_number = license_numbers[i]
                    license_validity = license_validities[i] if i < len(license_validities) else None

                    civil_service_eligibility = CivilServiceEligibility.objects.create(
                        name = str(latest_name + 1),
                        career_service=career_service,
                        rating=rating,
                        exam_date=exam_date,
                        exam_place=exam_place,
                        license_number=license_number,
                        license_validity=license_validity,
                    )
                    civil_service_eligibility.save()
                print("Civil Service Eligibility Saved!")

            elif section == 'voluntary_work':
                organization_names = request.POST.getlist('organization_name[]')
                from_dates = request.POST.getlist('from_date[]')
                to_dates = request.POST.getlist('to_date[]')
                number_of_hours = request.POST.getlist('number_of_hours[]')
                nature_of_works = request.POST.getlist('nature_of_work[]')
                latest_name = get_latest_name(VoluntaryWork)

                # Loop through each entry and save
                for i in range(len(organization_names)):
                    organization_name = organization_names[i]
                    from_date = from_dates[i] if i < len(from_dates) else None
                    to_date = to_dates[i] if i < len(to_dates) else None
                    number_of_hour = number_of_hours[i] if i < len(number_of_hours) else None
                    nature_of_work = nature_of_works[i]

                    voluntary_work = VoluntaryWork.objects.create(
                        name = str(latest_name + 1),
                        organization_name=organization_name,
                        from_date=from_date,
                        to_date=to_date,
                        number_of_hours=number_of_hour,
                        nature_of_work=nature_of_work,
                    )
                    voluntary_work.save()
                print("Voluntary Work Saved!")

            elif section == 'learning_and_development':
                titles = request.POST.getlist('title[]')
                from_dates = request.POST.getlist('from_date[]')
                to_dates = request.POST.getlist('to_date[]')
                number_of_hours = request.POST.getlist('number_of_hours[]')
                types_of_ld = request.POST.getlist('type_of_ld[]')
                conducted_bys = request.POST.getlist('conducted_by[]')
                latest_name = get_latest_name(LearningDevelopment)

                # Loop through each entry and save
                for i in range(len(titles)):
                    title = titles[i]
                    from_date = from_dates[i] if i < len(from_dates) else None
                    to_date = to_dates[i] if i < len(to_dates) else None
                    number_of_hour = number_of_hours[i] if i < len(number_of_hours) else None
                    type_of_ld = types_of_ld[i]
                    conducted_by = conducted_bys[i]

                    learning_development = LearningDevelopment.objects.create(
                        name = str(latest_name + 1),
                        title=title,
                        from_date=from_date,
                        to_date=to_date,
                        number_of_hours=number_of_hour,
                        type_of_ld=type_of_ld,
                        conducted_by=conducted_by,
                    )
                    learning_development.save()
                print("Learning and Development Saved!")

            elif section == 'work_experience':
                from_dates = request.POST.getlist('from_date[]')
                to_dates = request.POST.getlist('to_date[]')
                position_titles = request.POST.getlist('position_title[]')
                departments = request.POST.getlist('department[]')
                monthly_salaries = request.POST.getlist('monthly_salary[]')
                salary_grades = request.POST.getlist('salary_grade[]')
                status_of_appointments = request.POST.getlist('status_of_appointment[]')
                govt_services = request.POST.getlist('govt_service[]')
                latest_name = get_latest_name(WorkExperience)

                for i in range(len(from_dates)):
                    from_date = from_dates[i] if i < len(from_dates) else None
                    to_date = to_dates[i] if i < len(to_dates) else None
                    position_title = position_titles[i] if i < len(position_titles) else ''
                    department = departments[i] if i < len(departments) else ''
                    monthly_salary = monthly_salaries[i] if i < len(monthly_salaries) else None
                    salary_grade = salary_grades[i] if i < len(salary_grades) else None
                    status_of_appointment = status_of_appointments[i] if i < len(status_of_appointments) else ''
                    govt_service = govt_services[i] if i < len(govt_services) else 'N'  # Default to 'N' if not selected

                    work_experience = WorkExperience.objects.create(
                        name = str(latest_name + 1),
                        from_date=from_date,
                        to_date=to_date,
                        position_title=position_title,
                        department=department,
                        monthly_salary=monthly_salary,
                        salary_grade=salary_grade,
                        status_of_appointment=status_of_appointment,
                        govt_service=govt_service,
                    )
                    work_experience.save()
                print("Work Experience Saved!")

            

            
        sections_list = list(SECTIONS.keys())
        current_index = sections_list.index(section)
        if current_index + 1 < len(sections_list):
            next_section = sections_list[current_index + 1]
            return redirect('section_view', section=next_section)
        else:
            
            personal_info = get_latest(PersonalInformation)
            other_info = get_latest(OtherInformation)
            family = get_latest(FamilyBackground)
            education = get_latest(EducationalBackground)

            work = get_latest_objects(WorkExperience)
            learning = get_latest_objects(LearningDevelopment)
            civil = get_latest_objects(CivilServiceEligibility)
            voluntary = get_latest_objects(VoluntaryWork)

            complete_form = CompleteForm.objects.create(
                name=request.POST['form_name'],
                other_information=other_info,
                educational_background=education,
                personal_information = personal_info,
                family_background = family,
            )

            complete_form.voluntary_work.set(voluntary)
            complete_form.civil_service.set(civil)
            complete_form.learning_development.set(learning)
            complete_form.work_experience.set(work)

            complete_form.save()
            return redirect("/")

    context = {
        'active_section': section,
        'form': form,
        'SECTIONS': SECTIONS
    }

    return render(request, section_details['template'], context)


def all_forms(request, form_id):

    all_forms = CompleteForm.objects.all()
    form1 = CompleteForm.objects.get(id=form_id)

    return render(request,"pds_app/all_forms.html",{"form":form1, "forms":all_forms})


def forms(request):
    all_forms = CompleteForm.objects.all()


    return render(request,"pds_app/forms.html",{"forms":all_forms})

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


def home(request):
    forms1 = CompleteForm.objects.all()
    return render(request,"pds_app/forms.html",{"forms":forms1})


def create_form(request):

    return redirect('section_view', section='personal_info')
