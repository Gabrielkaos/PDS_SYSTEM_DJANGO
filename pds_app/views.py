from django.shortcuts import render, redirect
from .models import *
from .forms import PersonalInformationForm, FamilyBackgroundForm, EducationalBackgroundForm, OtherInformationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404


@login_required
def home(request):
    forms1 = CompleteForm.objects.filter(user=request.user)
    return render(request, "pds_app/forms.html", {"forms": forms1})
    # forms1 = CompleteForm.objects.all()
    # return render(request,"pds_app/forms.html",{"forms":forms1})

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

@login_required
def delete_form(request, form_id):
    """Ensure users can only delete their own forms"""
    form = get_object_or_404(CompleteForm, id=form_id, user=request.user)
    
    if request.method == "POST":
        form.delete()
        return redirect('home')
    
    return redirect('home')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def edit_form(request, form_id):
    form_instance = get_object_or_404(CompleteForm, id=form_id, user=request.user)
    
    if request.method == 'POST':
        print(request.POST)
        print("POST")
        personal_form = PersonalInformationForm(request.POST, instance=form_instance.personal_information)
        family_form = FamilyBackgroundForm(request.POST, instance=form_instance.family_background)
        education_form = EducationalBackgroundForm(request.POST, instance=form_instance.educational_background)
        other_form = OtherInformationForm(request.POST, instance=form_instance.other_information)

        print("Personal form errors:", personal_form.errors)
        print("Family form errors:", family_form.errors)
        print("Education form errors:", education_form.errors)
        print("Other form errors:", other_form.errors)

        print([personal_form.is_valid(), family_form.is_valid(), education_form.is_valid(), other_form.is_valid()])
        
        if all([personal_form.is_valid(), family_form.is_valid(), other_form.is_valid(),education_form.is_valid()]):

            personal_form.save()
            family_form.save()
            education_form.save()
            other_form.save()
            print("Saved")

            # save civil service eligibility
            # Delete existing civil service records
            form_instance.civil_service.all().delete()

            # Save new civil service records
            career_services = request.POST.getlist('career_service[]')
            ratings = request.POST.getlist('rating[]')
            exam_dates = request.POST.getlist('exam_date[]')
            exam_places = request.POST.getlist('exam_place[]')
            license_numbers = request.POST.getlist('license_number[]')
            license_validities = request.POST.getlist('license_validity[]')

            print("career_services:", request.POST.getlist('career_service[]'))
            print("ratings:", request.POST.getlist('rating[]'))
            print("exam_dates:", request.POST.getlist('exam_date[]'))
            print("exam_places:", request.POST.getlist('exam_place[]'))
            print("license_number:", request.POST.getlist('license_number[]'))
            print("license_validities:", request.POST.getlist('license_validity[]'))

            civil_services = []
            for i in range(len(career_services)):
                if career_services[i].strip():
                    civil_service = CivilServiceEligibility.objects.create(
                        user=request.user,
                        career_service=career_services[i],
                        rating=ratings[i] if i < len(ratings) else None,
                        exam_date=exam_dates[i] if i < len(exam_dates) else None,
                        exam_place=exam_places[i] if i < len(exam_places) else None,
                        license_number=license_numbers[i] if i < len(license_numbers) else None,
                        license_validity=license_validities[i] if i < len(license_validities) else None,
                    )
                    civil_services.append(civil_service)
            form_instance.civil_service.set(civil_services)


            # Delete and recreate Work Experience
            form_instance.work_experience.all().delete()
            work_from_dates = request.POST.getlist('work_from_date[]')
            work_experiences = []
            for i in range(len(work_from_dates)):
                if work_from_dates[i]:
                    work_exp = WorkExperience.objects.create(
                        user=request.user,
                        from_date=work_from_dates[i],
                        to_date=request.POST.getlist('work_to_date[]')[i] if i < len(request.POST.getlist('work_to_date[]')) and request.POST.getlist('work_to_date[]')[i] else None,
                        position_title=request.POST.getlist('work_position_title[]')[i] if i < len(request.POST.getlist('work_position_title[]')) else '',
                        department=request.POST.getlist('work_department[]')[i] if i < len(request.POST.getlist('work_department[]')) else '',
                        monthly_salary=request.POST.getlist('work_monthly_salary[]')[i] if i < len(request.POST.getlist('work_monthly_salary[]')) and request.POST.getlist('work_monthly_salary[]')[i] else None,
                        salary_grade=request.POST.getlist('work_salary_grade[]')[i] if i < len(request.POST.getlist('work_salary_grade[]')) else None,
                        status_of_appointment=request.POST.getlist('work_status[]')[i] if i < len(request.POST.getlist('work_status[]')) else '',
                        govt_service=request.POST.getlist('work_govt_service[]')[i] if i < len(request.POST.getlist('work_govt_service[]')) else 'N',
                    )
                    work_experiences.append(work_exp)
            form_instance.work_experience.set(work_experiences)

            # Delete and recreate Voluntary Work
            form_instance.voluntary_work.all().delete()
            voluntary_orgs = request.POST.getlist('voluntary_org[]')
            voluntary_works = []
            for i in range(len(voluntary_orgs)):
                if voluntary_orgs[i].strip():
                    voluntary = VoluntaryWork.objects.create(
                        user=request.user,
                        organization_name=voluntary_orgs[i],
                        from_date=request.POST.getlist('voluntary_from[]')[i] if i < len(request.POST.getlist('voluntary_from[]')) and request.POST.getlist('voluntary_from[]')[i] else None,
                        to_date=request.POST.getlist('voluntary_to[]')[i] if i < len(request.POST.getlist('voluntary_to[]')) and request.POST.getlist('voluntary_to[]')[i] else None,
                        number_of_hours=request.POST.getlist('voluntary_hours[]')[i] if i < len(request.POST.getlist('voluntary_hours[]')) and request.POST.getlist('voluntary_hours[]')[i] else 0,
                        nature_of_work=request.POST.getlist('voluntary_nature[]')[i] if i < len(request.POST.getlist('voluntary_nature[]')) else '',
                    )
                    voluntary_works.append(voluntary)
            form_instance.voluntary_work.set(voluntary_works)

            # Delete and recreate Learning Development
            form_instance.learning_development.all().delete()
            learning_titles = request.POST.getlist('learning_title[]')

            learning_developments = []
            for i in range(len(learning_titles)):
                if learning_titles[i].strip():
                    learning = LearningDevelopment.objects.create(
                        user=request.user,
                        title=learning_titles[i],
                        from_date=request.POST.getlist('learning_from[]')[i] if i < len(request.POST.getlist('learning_from[]')) and request.POST.getlist('learning_from[]')[i] else None,
                        to_date=request.POST.getlist('learning_to[]')[i] if i < len(request.POST.getlist('learning_to[]')) and request.POST.getlist('learning_to[]')[i] else None,
                        number_of_hours=request.POST.getlist('learning_hours[]')[i] if i < len(request.POST.getlist('learning_hours[]')) and request.POST.getlist('learning_hours[]')[i] else 0,
                        type_of_ld=request.POST.getlist('learning_type[]')[i] if i < len(request.POST.getlist('learning_type[]')) else '',
                        conducted_by=request.POST.getlist('learning_conducted[]')[i] if i < len(request.POST.getlist('learning_conducted[]')) else '',
                    )
                    learning_developments.append(learning)
            form_instance.learning_development.set(learning_developments)

                        
            # Update form name if provided
            if 'form_name' in request.POST:
                form_instance.save()
                print("saved form name")
            
            return redirect('all_forms', form_id=form_id)


        else:
            for form in [personal_form, family_form, education_form, other_form]:
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{form[field].label}: {error}")
    else:
        # Pre-populate forms with existing data
        personal_form = PersonalInformationForm(instance=form_instance.personal_information)
        family_form = FamilyBackgroundForm(instance=form_instance.family_background)
        education_form = EducationalBackgroundForm(instance=form_instance.educational_background)
        other_form = OtherInformationForm(instance=form_instance.other_information)
    
    print(form_instance.civil_service.all)
    context = {
        'form_instance': form_instance,
        'personal_form': personal_form,
        'family_form': family_form,
        'education_form': education_form,
        'other_form': other_form,
        'creating': False,
        "forms" : CompleteForm.objects.filter(user=request.user)
    }
    
    return render(request, 'pds_app/edit_form.html', context)

@login_required
def create_form(request):
    if request.method == 'POST':
        personal_form = PersonalInformationForm(request.POST)
        family_form = FamilyBackgroundForm(request.POST)
        education_form = EducationalBackgroundForm(request.POST)
        other_form = OtherInformationForm(request.POST)

        print("Personal form errors:", personal_form.errors)
        print("Family form errors:", family_form.errors)
        print("Education form errors:", education_form.errors)
        print("Other form errors:", other_form.errors)

        print([personal_form.is_valid(), family_form.is_valid(), education_form.is_valid(), other_form.is_valid()])
        
        if all([personal_form.is_valid(), family_form.is_valid(), other_form.is_valid(),education_form.is_valid()]):

            personal_inst = personal_form.save(commit=False)
            family_inst = family_form.save(commit=False)
            education_inst = education_form.save(commit=False)
            other_inst = other_form.save(commit=False)

            for inst in [personal_inst, family_inst, education_inst, other_inst]:
                inst.user = request.user
                inst.save()
            print("Saved")

            

            # Save ManyToMany related objects
            # Civil Service Eligibility
            career_services = request.POST.getlist('career_service[]')
            ratings = request.POST.getlist('rating[]')
            exam_dates = request.POST.getlist('exam_date[]')
            exam_places = request.POST.getlist('exam_place[]')
            license_numbers = request.POST.getlist('license_number[]')
            license_validities = request.POST.getlist('license_validity[]')
            civil_services = []
            for i in range(len(career_services)):
                if career_services[i].strip():
                    civil_service = CivilServiceEligibility.objects.create(
                        user=request.user,
                        career_service=career_services[i],
                        rating=ratings[i] if i < len(ratings) else None,
                        exam_date=exam_dates[i] if i < len(exam_dates) else None,
                        exam_place=exam_places[i] if i < len(exam_places) else None,
                        license_number=license_numbers[i] if i < len(license_numbers) else None,
                        license_validity=license_validities[i] if i < len(license_validities) else None,
                    )
                    civil_services.append(civil_service)
            

            # Work Experience
            work_from_dates = request.POST.getlist('work_from_date[]')
            work_experiences = []
            for i in range(len(work_from_dates)):
                if work_from_dates[i]:
                    work_exp = WorkExperience.objects.create(
                        user=request.user,
                        from_date=work_from_dates[i],
                        to_date=request.POST.getlist('work_to_date[]')[i] if i < len(request.POST.getlist('work_to_date[]')) and request.POST.getlist('work_to_date[]')[i] else None,
                        position_title=request.POST.getlist('work_position_title[]')[i] if i < len(request.POST.getlist('work_position_title[]')) else '',
                        department=request.POST.getlist('work_department[]')[i] if i < len(request.POST.getlist('work_department[]')) else '',
                        monthly_salary=request.POST.getlist('work_monthly_salary[]')[i] if i < len(request.POST.getlist('work_monthly_salary[]')) and request.POST.getlist('work_monthly_salary[]')[i] else None,
                        salary_grade=request.POST.getlist('work_salary_grade[]')[i] if i < len(request.POST.getlist('work_salary_grade[]')) else None,
                        status_of_appointment=request.POST.getlist('work_status[]')[i] if i < len(request.POST.getlist('work_status[]')) else '',
                        govt_service=request.POST.getlist('work_govt_service[]')[i] if i < len(request.POST.getlist('work_govt_service[]')) else 'N',
                    )
                    work_experiences.append(work_exp)

            # Voluntary Work
            voluntary_orgs = request.POST.getlist('voluntary_org[]')
            voluntary_works = []
            for i in range(len(voluntary_orgs)):
                if voluntary_orgs[i].strip():
                    voluntary = VoluntaryWork.objects.create(
                        user=request.user,
                        organization_name=voluntary_orgs[i],
                        from_date=request.POST.getlist('voluntary_from[]')[i] if i < len(request.POST.getlist('voluntary_from[]')) and request.POST.getlist('voluntary_from[]')[i] else None,
                        to_date=request.POST.getlist('voluntary_to[]')[i] if i < len(request.POST.getlist('voluntary_to[]')) and request.POST.getlist('voluntary_to[]')[i] else None,
                        number_of_hours=request.POST.getlist('voluntary_hours[]')[i] if i < len(request.POST.getlist('voluntary_hours[]')) and request.POST.getlist('voluntary_hours[]')[i] else 0,
                        nature_of_work=request.POST.getlist('voluntary_nature[]')[i] if i < len(request.POST.getlist('voluntary_nature[]')) else '',
                    )
                    voluntary_works.append(voluntary)

            # Learning and Development
            learning_titles = request.POST.getlist('learning_title[]')
            learning_developments = []
            for i in range(len(learning_titles)):
                if learning_titles[i].strip():
                    learning = LearningDevelopment.objects.create(
                        user=request.user,
                        title=learning_titles[i],
                        from_date=request.POST.getlist('learning_from[]')[i] if i < len(request.POST.getlist('learning_from[]')) and request.POST.getlist('learning_from[]')[i] else None,
                        to_date=request.POST.getlist('learning_to[]')[i] if i < len(request.POST.getlist('learning_to[]')) and request.POST.getlist('learning_to[]')[i] else None,
                        number_of_hours=request.POST.getlist('learning_hours[]')[i] if i < len(request.POST.getlist('learning_hours[]')) and request.POST.getlist('learning_hours[]')[i] else 0,
                        type_of_ld=request.POST.getlist('learning_type[]')[i] if i < len(request.POST.getlist('learning_type[]')) else '',
                        conducted_by=request.POST.getlist('learning_conducted[]')[i] if i < len(request.POST.getlist('learning_conducted[]')) else '',
                    )
                    learning_developments.append(learning)

            # Create the CompleteForm instance and save related objects after
            complete_form = CompleteForm.objects.create(
                user=request.user,
                personal_information=personal_inst,
                family_background=family_inst,
                educational_background=education_inst,
                other_information=other_inst
            )
            complete_form.civil_service.set(civil_services)
            complete_form.work_experience.set(work_experiences)
            complete_form.voluntary_work.set(voluntary_works)
            complete_form.learning_development.set(learning_developments)


            return redirect('home')
        else:
            for form in [personal_form, family_form, education_form, other_form]:
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{form[field].label}: {error}")

    else:
        # Pre-populate empty forms
        personal_form = PersonalInformationForm()
        family_form = FamilyBackgroundForm()
        education_form = EducationalBackgroundForm()
        other_form = OtherInformationForm()

    context = {
        'personal_form': personal_form,
        'family_form': family_form,
        'education_form': education_form,
        'other_form': other_form,
        'creating': True,
        "forms": CompleteForm.objects.filter(user=request.user)
    }

    return render(request, 'pds_app/edit_form.html', context)
