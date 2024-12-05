from django.contrib import admin


from .models import *


admin.site.register(PersonalInformation)
admin.site.register(FamilyBackground)
admin.site.register(EducationalBackground)
admin.site.register(CivilServiceEligibility)
admin.site.register(VoluntaryWork)
admin.site.register(LearningDevelopment)
admin.site.register(WorkExperience)
admin.site.register(CompleteForm)
admin.site.register(OtherInformation)